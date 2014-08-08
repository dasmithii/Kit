# Lists paths to all files within.
def files_under(directory):
	ret = []
	for root, dirs, files in os.walk(directory):
		for path in files:
			ret.append(path)
	return ret