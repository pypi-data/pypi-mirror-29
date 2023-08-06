from __future__ import absolute_import
from json import dumps as json_dumps
import logging
import logging.handlers
import sys

LOG = logging.getLogger(__name__)


class JsonFormatter(logging.Formatter):
	DEFAULT_FIELDS = ('levelname', 'name', 'msg')

	def __init__(self, fields=None, datefmt=None):
		super(JsonFormatter, self).__init__(datefmt=datefmt)
		self.fields = tuple(fields) if fields else self.DEFAULT_FIELDS

	def format(self, record):
		data = {}
		for key in record.__dict__:
			if key in self.fields:
				data[key] = getattr(record, key)
		data['time'] = self.formatTime(record)
		return json_dumps(data)


def get_formatter(colors, shortened_levels=True):
	level_len = 5 if shortened_levels else 8
	if colors:
		level_len += 11
		fmt = '\033[37m%(asctime)s %(levelname_colored)' + str(level_len) + \
			's\033[37m %(name)s \033[0m%(message)s'
	else:
		fmt = '%(asctime)s [%(levelname)' + str(level_len) + 's] [%(name)s] %(message)s'
	return logging.Formatter(fmt)


class ColorLogRecord(logging.LogRecord):
	RESET = '\033[0m'
	BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = (
		'\033[1;%dm' % (i + 30) for i in range(8)
	)

	COLORS = {
		logging.DEBUG: GREEN,
		logging.INFO: BLUE,
		logging.WARNING: MAGENTA,
		logging.ERROR: YELLOW,
		logging.CRITICAL: RED,
	}

	def __init__(self, *args, **kwargs):
		super(ColorLogRecord, self).__init__(*args, **kwargs)
		self.levelname_colored = '%s%s%s' % (
			self.COLORS[self.levelno],
			self.levelname,
			self.RESET,
		)


def _shorten_levels():
	#pylint: disable=no-member,protected-access
	if hasattr(logging, '_levelNames'):
		# python 2.7, 3.3
		logging._levelNames[logging.WARNING] = 'WARN'
		logging._levelNames['WARN'] = logging.WARNING
		logging._levelNames[logging.CRITICAL] = 'CRIT'
		logging._levelNames['CRIT'] = logging.CRITICAL
	else:
		# python 3.4+
		logging._levelToName[logging.WARNING] = 'WARN'
		logging._nameToLevel['WARN'] = logging.WARNING
		logging._levelToName[logging.CRITICAL] = 'CRIT'
		logging._nameToLevel['CRIT'] = logging.CRITICAL
	#pylint: enable=no-member,protected-access


def _level(level):
	if isinstance(level, (str, bytes)):
		return logging.getLevelName(level.upper())
	return level


class LogSetup:
	"""
	Class that makes it easy to set up many different types of loggers.

	ls = LogSetup()
	ls.add_file('/var/log/myapp.log', logging.WARNING)
	ls.add_file('/var/log/myapp-debug.log', logging.DEBUG)
	ls.add_console(logging.INFO)
	ls.finish()
	"""
	def __init__(
		self,
		default_level=logging.WARNING,
		root_level=logging.DEBUG,
		colors=False,
		shorten_levels=False,
	):
		"""
		Args:
			root_level: Which level to set on the root logger. If this is set,
				levels lower than this will be ignored even if set on individual
				handlers, so it's usually a good idea to leave this at DEBUG.
			default_level: Which level to set for loggers by default.
			colors: Use colors in console logging if possible.
			shorten_levels: Shorten long log level names.
		"""
		self.default_level = _level(default_level)
		self.root_level = _level(root_level)
		self.shorten_levels = shorten_levels
		self.startup_messages = []
		self.handlers = []
		self._finished = False

		self.colors = False
		if colors:
			if hasattr(logging, 'setLogRecordFactory'):
				logging.setLogRecordFactory(ColorLogRecord) #pylint: disable=no-member
				self.colors = True
			else:
				self.add_startup_message(
					logging.WARNING,
					'color logging not supported in python2, sorry',
				)

		if self.shorten_levels:
			_shorten_levels()

	def add_handler(self, handler):
		"""
		Add a pre-configured handler to the setup.
		"""
		if self._finished:
			raise RuntimeError('cannot add handler, logging already set up')
		self.handlers.append(handler)

	def add_startup_message(self, level, message, *args):
		"""
		Add a line to be logged once logging has been set up.
		"""
		if self._finished:
			raise RuntimeError('cannot add startup message, logging already set up')
		self.startup_messages.append((level, message) + args)

	def add_file(self, file, level=None, json=False, json_fields=None):
		"""
		Log to a file.
		"""
		if self._finished:
			raise RuntimeError('cannot add handler, logging already set up')

		if file.lower() == 'stderr':
			handler = logging.StreamHandler(sys.stderr)
			file = 'STDERR'
		elif file.lower() == 'stdout':
			handler = logging.StreamHandler(sys.stdout)
			file = 'STDOUT'
		elif file:
			handler = logging.handlers.WatchedFileHandler(file)

		if json:
			formatter = JsonFormatter(fields=json_fields)
		else:
			# define the logging format
			formatter = get_formatter(
				colors=self.colors and file in ('STDERR', 'STDOUT'),
				shortened_levels=self.shorten_levels,
			)
		handler.setFormatter(formatter)

		if level is None:
			level = self.default_level
		else:
			level = _level(level)
		handler.setLevel(level)

		self.add_startup_message(
			logging.INFO,
			'setting up log handler %r to %s with level %s',
			handler, file, level,
		)
		self.add_handler(handler)

	def add_json(self, file, level=None, fields=None):
		"""
		Log in a JSON format to a file.
		"""
		self.add_file(file, level=level, json=True, json_fields=fields)

	def add_console(self, level=None, check_interactive=True):
		"""
		Log to the console/terminal.
		Args:
			level: The log level.
			check_interactive: If True, checks if stderr is a TTY, and only sets
				up logging if it is.
		"""
		if self._finished:
			raise RuntimeError('cannot add handler, logging already set up')

		if check_interactive and not sys.__stderr__.isatty(): #pylint: disable=no-member
			self.add_startup_message(
				logging.INFO,
				'sys.stderr is not a TTY, not logging to it',
			)
			return
		self.add_file('stderr', level=level)

	def finish(self):
		"""
		Complete logging setup.
		"""
		if self._finished:
			raise RuntimeError('logging already set up')

		root = logging.getLogger()
		if self.root_level:
			root.setLevel(self.root_level)

		for handler in self.handlers:
			root.addHandler(handler)

		for line in self.startup_messages:
			level, message = line[:2]
			args = line[2:]
			LOG.log(level, message, *args)

		self._finished = True


def setup_logging(
	log_file=None,
	log_level=None,
	check_interactive=None,
	json=False,
	json_fields=None,
	colors=False,
	shorten_levels=True,
):
	log_setup = LogSetup(default_level=log_level, colors=colors, shorten_levels=shorten_levels)
	log_setup.add_file(log_file or 'stderr', json=json, json_fields=json_fields)
	if log_file and log_file.lower() not in ('stderr', 'stdout'):
		log_setup.add_console(check_interactive=check_interactive)
	log_setup.finish()
