import os


# Gathers files recursively.
def files_under(directory):
	ret = []
	for root, dirs, files in os.walk(directory):
		for path in files:
			path = root + '/' + '/'.join(dirs) + '/' + path
			path = path.replace('//', '/')
			ret.append(path)
	return ret


# Gathers .c files recursively.
def sources_under(directory):
	files = files_under(directory)
	return filter(lambda x: x.endswith(('.h', '.c')), files)


# Gathers .h files recursively.
def headers_under(directory):
	files = files_under(directory)
	return filter(lambda x: x.endswith('.h'), files)


# Creates file.
def touch(path):
	os.system('touch ' + path)


# Converts from textual color to ANSI code for printing in terminal.
def compile_ansi(color):
	options = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
	index = options.index(color)
	if index == -1:
		raise 'non-supported color'
	else:
		return index + 30


# Wraps given text with begin/end ANSI codes by number.
def color_with_code(text, code):
	return "\033[" + str(code) + "m" + text + "\033[0m"


# Same as above but by textual color.
def color(text, color):
	code = compile_ansi(color)
	return color_with_code(text, code)