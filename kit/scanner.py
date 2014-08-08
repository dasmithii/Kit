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

def extract_name(s):
	return s[s.find('kit/') + 4 : s.find('>')]



# Extracts included kit module names.
def text_references(text):
	lines = text.split('\n')
	includes = filter(is_dependency, lines)
	return Set(map(extract_name, includes))

# Wrapper for above.
def file_references(path):
	with open(path, 'r') as f:
		return text_references(f.read())

# Scans project sources and their dependencies recursively, returning
# a set of kit modules to include.
def directory_references(root):
	refs = Set()
	for path in sources_under(root):
		refs += file_references(path)
	return refs

def module_references(name):
	path = storage.module_path(name)
	return directory_references(path)

def directory_dependencies(path):
	deps = directory_references(path)
	while True:
		prev = deps
		deps = reduce(operator.add, map(module_references, deps))
		if len(prev) == len(deps):
			return deps

def module_dependencies(name):
	path = storage.module_path(name)
	return directory_dependencies(path)


