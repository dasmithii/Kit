import os
import urllib
from utility import *

root = '/usr/local/kit'
modules = root + '/modules'
headers = root + '/headers'
module_list = modules + '/list.csv'
remote_index_url = 'https://raw.github.com/dasmithii/Kit/master/MODULES.csv'


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
	parts = map(str.strip, line.split(','))
	return tuple(parts[0:2])

def local_modules():
	with open(module_list, 'r') as f:
		lines = f.read().split('\n')
		return map(module_tuple, lines)

def remote_modules():
	try:
		index = urllib.urlopen(remote_index_url)
		lines = index.read().split('\n')
		return map(module_tuple, lines)
	except:
		print " > failed to retrieve module index."
		return []

def remote_resolve(name):
	mods = filter(lambda t: t[0] == name, remote_modules())[0]
	if len(mods) > 0:
		return mods[1]

def module_path(name):
	return modules + '/' + name

def module_source_path(name):
	return module_path(name) + '/sources'

def module_sources(name):
	return sources_under(module_path(name))

