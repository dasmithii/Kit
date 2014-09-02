import os
import sys
import shutil
import utility
import storage
import scanner
import builder
import subprocess

HELLO_WORLD = '''#include <stdio.h>

int main()
{
    printf("Hello, world!");
}
'''




def output_name(path):
    return os.path.abspath(path).split('/')[-1]


# Deletes on compilation products.
def clean(path):
    shutil.rmtree(path + '/build', ignore_errors=True)


# Compiles directory.
def build(path):
    builder.build_directory(path)


# Geneerates a self-contained C project [which doesn't depend
# on kit] and places it in build/dist.
def dist(path):
    print utility.color('TODO: command `dist` has not yet been implemented', 'red')


# Attempts to clone repository from remote index.
def fetch(arg):
    if arg == 'all':
        for name in storage.remote_module_names():
            if not storage.contains_module(name):
                fetch(name)
            else:
                print ' - module', name, 'is already installed'
    elif arg.find('.git') >= 0:
        storage.fetch_unindexed_module(arg)
    else:
        storage.fetch_module(arg)


# Deletes module with given name from local index.
def remove(path):
    print 'removing', path
    if path.find(storage.modules) == 0:
        name = path.split('/')[-1]
        storage.clear_module(name)
    else:
        shutil.rmtree(path, ignore_errors=True)


# Sets up boilerplate project structure.
def init(path):
    wd = os.getcwd()
    os.chdir(path)
    os.makedirs('documentation')
    os.makedirs('sources')
    os.makedirs('tests')
    os.makedirs('documentation/generated')
    utility.touch('README.md')
    utility.touch('LICENSE.md')
    with open('sources/main.c', 'w') as f:
        f.write(HELLO_WORLD)
    with open('tests/main.c', 'w') as f:
        f.write(HELLO_WORLD)
    with open('.gitignore', 'w') as f:
        f.write('build\n')
    os.chdir(wd)


# If building an application, its executable is made available
# globally. Regardless, the library is placed in the local index.
def install(path):
    build(path)
    name = os.path.abspath(path).split('/')[-1]
    if scanner.has_main(path):
        shutil.copy('build/bin/' + name, '/usr/local/bin/' + name)
    dest = storage.module_path(name)
    shutil.copytree(path, dest)
    storage.index(name, 'none')
    execute('clean', name)
    execute('build', name)


# Lists available modules (both local and remote).
def modules(arg):
    local = storage.local_modules()
    print 'local:  (' + str(len(local)) + ')'
    for m in local:
        if storage.module_compiled(m[0]):
            print ' - ' + m[0], '[' + utility.color('compiled', 'green') + ']'
        else:
            print ' - ' + m[0], '[' + utility.color('not compiled', 'red') + ']'

    if arg == 'all':
        remote = storage.remote_modules()
        print '\nremote:  (' + str(len(remote)) + ')'
        for m in remote:
            print ' -', m[0], '[' + utility.color(m[1], 'yellow') + ']'


# Builds and runs generated executable.
def run(path):
    if scanner.has_main('.'):
        build('.')
        name = output_name('.')
        subprocess.call(['./build/bin/' + name] + sys.argv[2:])
    else:
        print utility.color("- ERROR: this project doesn't produce an executable, and thus it cannot be run.", 'red')


# Builds target and runs its tests.
def test(path):
    build(path)
    subprocess.call(path + '/build/bin/tests')


# Hack.
def execute(command, argument):
    if command in ['fetch', 'modules']:
        globals()[command](argument)
    elif argument == 'all':
        print ' - detected ALL'
        for module in storage.local_module_names():
            execute(command, module)
    else:
        path = os.path.abspath('.')
        if argument:
            path = storage.module_path(argument)
        try:
            globals()[command](path)
        except:
            print utility.color(' - ERROR: command not available', 'red')
