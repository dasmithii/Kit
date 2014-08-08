import os
from utility import *

root = '/usr/local/kit'
modules = root + '/modules'
headers = root + '/headers'
module_list = modules + '/list.csv'


def ready():
	return os.path.exists(root)

def setup():
	os.makedirs(root)
	os.makedirs(modules)
	os.makedirs(headers)
	with open(module_list, 'w+') as f:
		f.write('base, https://github.com/dasmithii/BaseKit')

def ensure_ready():
	if not ready():
		setup()

def module_tuple(line):
	s = line.split(',')
	return (parts[0], parts[1].lstrip())

def available_modules():
	with open(module_list, 'r') as f:
		lines = f.read().split('\n')
		return map(module_tuple, lines)

def module_path(name):
	return modules + '/' + name

def module_source_path(name):
	return module_path(name) + '/sources'

def module_sources(name):
	return sources_under(module_path(name))