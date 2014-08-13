import operator
import storage
from utility import *
from sets import Set



# Utility functions for scanning include statements.
def has_pound(s):
	return s[0:1] == '#'

def has_kit(s):
	return s.find('<kit/') >= 0

def is_dependency(s):
	return has_pound(s) and has_kit(s)


# Parses kit include statement (as follows).
# '#include <kit/module/file.h>'  =>  'base/module/file.h'
# '#include <kit/file.h>'         =>  'base/file/file.h'
def extract_reference(s):
	main = s[s.find('kit/') + 4 : s.find('>')]
	if main.count('/') == 0:
		main = main[0:main.find('.')] + main
	return main


# Extracts paths included in format: #include <kit/module/file.h>, which
# becomes "module/file.h".
def text_references(text):
	lines = text.split('\n')
	includes = filter(is_dependency, lines)
	return Set(map(extract_reference, includes))

# Wrapper for above.
def file_references(path):
	with open(path, 'r') as f:
		return text_references(f.read())

# Scans project sources and their dependencies recursively, returning
# a set of kit modules to include.
def directory_references(root):
	refs = Set()
	for path in sources_under(root):
		refs |= file_references(path)
	return refs

# Wrapper for above, but with a locally indexed module.
def module_references(name):
	path = storage.module_path(name)
	return directory_references(path)

# Given references to files in the Kit module index, returns
# a set of required modules.
def deps_from_references(refs):
	ret = Set()
	for ref in refs:
		ret.add(ref.split('/')[0])
	return ret

# Shallow dependencies of kit project with root path.
def directory_dependencies(path):
	refs = directory_references(path)
	return deps_from_references(refs)

# Shallow dependencies of kit module in index with name.
def module_dependencies(name):
	path = storage.module_path(name)
	return directory_dependencies(path)


