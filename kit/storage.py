import os
import urllib
import shutil
import logging
from utility import *


# Some helpful paths.
modules = '/usr/local/kit'
headers = modules + '/headers'
module_list = modules + '/list.csv'
remote_index_url = 'https://raw.github.com/dasmithii/Kit/master/MODULES.csv'


# Checks if storage directory has already been set up.
def ready():
	return os.path.exists(modules)


# Removes storage directory entirely.
def clear():
	if ready():
		shutil.rmtree(modules)


# Creates necessary files and directories. This should be
# run before Kit features are used.
def setup():
	clear()
	os.makedirs(modules)
	os.makedirs(modules + '/' + 'headers')
	os.makedirs(modules + '/' + 'headers/kit')
	with open(module_list, 'w+') as f:
		f.write('')


# Runs setup if not done already.
def ensure_ready():
	if not ready():
		setup()


# Parses line of index file.
def module_tuple(line):
	parts = map(str.strip, line.split(','))
	return tuple(parts[0:2])


# Parses index file.
def module_tuples(text):
	lines = filter(None, text.split('\n'))
	return map(module_tuple, lines)


# Parses local index. 
def local_modules():
	ensure_ready()
	with open(module_list, 'r') as f:
		return module_tuples(f.read())


# Parses remote index.
def remote_modules():
	try:
		index = urllib.urlopen(remote_index_url)
		return module_tuples(index.read())
	except:
		logging.info("failed to retrieve module index")
		return []


# Fetches git repository of module with given name in central
# index. 
def remote_resolve(name):
	mods = filter(lambda t: t[0] == name, remote_modules())[0]
	if len(mods) > 0:
		return mods[1]
	raise "couldn't resolve module with name " + name


# Path to module in central index.
def module_path(name):
	return modules + '/' + name


# Path to directory of consolidated headers. These are added to the
# include path of projects built with Kit.
def module_header_path(name):
	return module_path(name) + '/build/headers'


def module_source_path(name):
	return module_path(name) + '/sources'

def module_library_path(name):
	base = module_path(name) + '/build/bin/lib' + name
	return base + '.a'

def module_sources(name):
	return sources_under(module_path(name))


# Include module in the local registry.
def index(name, url):
	with open(module_list, 'a') as f:
		f.write('\n' + name + ', ' + url)


# Reverse above operation.
def unindex(name):
	mods = filter(lambda t: t[0] != name, local_modules())
	with open(module_list, 'w') as f:
		f.writelines(map(', '.join, mods)) 


# Check if module is indexed.
def contains_module(name):
	return os.path.exists(module_path(name))


# Check if available in central registry.
def remote_contains_module(name):
	if remote_resolve(name):
		return True
	return False


def module_compiled(name):
	root = module_path(name)
	return os.path.exists(root + '/build')


# Remove build products.
def clear_module(name):
	if contains_module(name):
		shutil.rmtree(module_path(name))
		unindex(name)


# Fetches module from someone's personal git repository.
def fetch_unindexed_module(repo):
	name = repo.split('/')[-1].replace('.git', '')
	clear_module(name)
	os.system('git clone ' + url + ' ' + modules + '/' + name)
	index(name, url)


# Fetches from central index.
def fetch_module(name):
	clear_module(name)
	url = remote_resolve(name)
	if not url:
		logging.error("failed to fetch module " + name)
	else:
		os.system('git clone ' + url + ' ' + modules + '/' + name)
		index(name, url)


