import os
import urllib
import shutil
import utility


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
    print utility.color(' - setup kit storage', 'green')


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


def local_module_names():
    return map(lambda x: x[0], local_modules())


# Parses remote index.
def remote_modules():
    try:
        index = urllib.urlopen(remote_index_url)
        return module_tuples(index.read())
    except:
        print utility.color(' - failed to retrieve remote index', 'red')
        return []


def remote_module_names():
    return map(lambda x: x[0], remote_modules())


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


def module_header_paths(name):
    path = storage.module_header_path(name)
    return utility.headers_under(path)


def module_source_path(name):
    return module_path(name) + '/sources'


def module_library_path(name):
    base = module_path(name) + '/build/bin/lib' + name
    return base + '_static.a'


def module_sources(name):
    return sources_under(module_path(name))


# Include module in the local registry.
def index(name, url):
    with open(module_list, 'a') as f:
        f.write('\n' + name + ', ' + url)
    print utility.color(' - indexed module: ' + name, 'green')


# Reverse above operation.
def unindex(name):
    s = ''
    for module in local_modules():
        if module[0] != name:
            s += ', '.join(module) + '\n'
    with open(module_list, 'w') as f:
        f.write(s[0:-1])


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
        print ' - deleted module:', name


# Fetches module from someone's personal git repository.
def fetch_unindexed_module(repo):
    name = repo.split('/')[-1].replace('.git', '')
    clear_module(name)
    if 0 == os.system('git clone ' + repo + ' ' + modules + '/' + name):
        print utility.color(' - cloned module successfully', 'green')
        index(name, repo)
    else:
        print utility.color(' - failed to fetch module: ' + name, 'red')


# Fetches from central index.
def fetch_module(name):
    clear_module(name)
    url = remote_resolve(name)
    if url and 0 == os.system('git clone ' + url + ' ' + modules + '/' + name):
        print utility.color(' - cloned module successfully', 'green')
        index(name, url)
    else:
        print utility.color(' - failed to fetch module: ' + name, 'red')
