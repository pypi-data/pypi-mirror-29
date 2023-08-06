import sys

from ..data import merge_dicts
from .spec import ArgumentSpec
from .config import get_config
from .argparser import parse_from_spec

__all__ = ('CommandLineInterface', 'ArgumentSpec')


class CommandLineInterface:
	def __init__(self, spec: ArgumentSpec, default_config_path=None):
		self.spec = spec
		self.default_config_path = default_config_path

	def get_options(self, args=None):
		if args is None:
			args = sys.argv[1:]
		parsed_args = parse_from_spec(self.spec, args)
		config = get_config(parsed_args, self.default_config_path)
		return merge_dicts(dict(parsed_args), config)
