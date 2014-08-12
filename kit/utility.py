import os

def files_under(directory):
	ret = []
	for root, dirs, files in os.walk(directory):
		for path in files:
			path = root + '/' + '/'.join(dirs) + '/' + path
			path = path.replace('//', '/')
			ret.append(path)
	return ret

def sources_under(directory):
	files = files_under(directory)
	return filter(lambda x: x.endswith(('.h', '.c')), files)

def headers_under(directory):
	files = files_under(directory)
	return filter(lambda x: x.endswith('.h'), files)

def touch(path):
	os.system('touch ' + path)


def compile(color):
	options = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
	index = options.index(color)
	if index == -1:
		raise 'non-supported color'
	else:
		return index + 30

def color_with_code(text, code):
	return "\033[" + str(code) + "m" + text + "\033[0m"

def color(text, color):
	code = compile(color)
	return color_with_code(text, code)