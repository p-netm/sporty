"""Define custom Errors, its really just that basic"""


class TagError(Exception):
	"""
	This is raised when the system fails to locate a required vital 
	html tag
	"""
	pass

# validationError  as validation error


class PatternMatchError(Exception):
	"""
	happens when a regular expression fails to match a string that
	the system expects should match"""
	pass
