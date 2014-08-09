# Lists paths to all files within.
def files_under(directory):
	ret = []
	for root, dirs, files in os.walk(directory):
		for path in files:
			ret.append(path)
	return ret

def sources_under(directory):
	files = files_under(directory)
	return filter(lambda x: x.endswith(('.h', '.c')), files)

def headers_under(directory):
	files = files_under(directory)
	return filter(lambda x: x.endswith('.h'), files)