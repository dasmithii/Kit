import os
import sys
import shutil
import utility
import storage
import scanner
import builder
import subprocess
import platform
from subprocess import Popen, PIPE

DEFAULT_APP_CODE = '''
#include <stdio.h>


int main()
{
    printf("Hello, world!");
}
'''


DEFAULT_TEST_CODE = '''
#include <kit/greatest.h>


GREATEST_MAIN_DEFS();
int main(int argc, char *argv[]) {
    GREATEST_MAIN_BEGIN();   
    GREATEST_MAIN_END();
    return 0;
}
'''




def output_name(path):
    return os.path.abspath(path).split('/')[-1]


# Deletes on compilation products.
def clean(path):
    shutil.rmtree(path + '/build', ignore_errors=True)
    try:
        os.remove(path + '/CMakeLists.txt')
    except OSError:
        pass

# Compiles directory.
def build(path, options=None):
    if not path:
        path = '.'
    builder.build_directory(path,options)

# Generates a self-contained C project [which doesn't depend
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
        f.write(DEFAULT_APP_CODE)
    with open('tests/main.c', 'w') as f:
        f.write(DEFAULT_TEST_CODE)
    with open('.gitignore', 'w') as f:
        f.write('build\n')
    os.chdir(wd)


# If building an application, its executable is made available
# globally. Regardless, the library is placed in the local index.
def install(path):
    build('.')
    name = os.path.abspath('.').split('/')[-1]
    if scanner.has_main('.'):
        shutil.copy('build/bin/' + name, '/usr/local/bin/' + name)
    dest = storage.module_path(name)
    shutil.copytree('.', dest)
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
        r = subprocess.call(['./build/bin/' + name] + sys.argv[2:])
        exit(r)
    else:
        print utility.color("- ERROR: this project doesn't produce an executable, and thus it cannot be run.", 'red')


# Builds target and runs its tests.
def test(path,options):
    build(path,options)
    args = [path + '/build/bin/tests']
    if 'debug' in options:
        if "Darwin" in platform.platform():
            args = ["lldb"] + args 
        else:
            args = ["gdb"] + args 
    if 'verbose' in options:
        print command_string
    r = subprocess.call(args)
    exit(r)


# Hack.
def execute(command, argument, options):
    if argument == 'all':
        for module in storage.local_module_names():
            execute(command, module, None)
    else:
        path = storage.module_path(argument) if argument else os.path.abspath('.')
        if command in ['test', 'build']:
            globals()[command](path, options)
        elif command in globals():
            globals()[command](path)
        else:
            print utility.color(' - ERROR: command not available', 'red')
