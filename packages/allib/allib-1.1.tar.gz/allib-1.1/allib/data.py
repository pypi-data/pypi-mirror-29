from copy import deepcopy


def update_dict(old_dict, new_dict):
	"""
	Update a dict in-place with values from another dict, recursively.
	"""
	for key, value in new_dict.items():
		if key in old_dict and isinstance(old_dict[key], dict) and isinstance(value, dict):
			update_dict(old_dict[key], value)
		else:
			old_dict[key] = value


def merge_dicts(old_dict, new_dict, deep=True):
	"""
	Create a new dict with recursively merged values from 2 existing dicts,
	without modifying the existing dicts.
	"""
	if deep:
		old_dict = deepcopy(old_dict)
	else:
		old_dict = old_dict.copy()

	update_dict(old_dict, new_dict)

	return old_dict
