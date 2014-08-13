import os
import shutil
import utility
import storage
import builder

# Deletes on compilation products.
def clean(context):
	shutil.rmtree('build', ignore_errors=True)


# Compiles current directory.
def build(context):
	builder.build_directory('.')


# Geneerates a self-contained C project [which doesn't depend
# on kit] and places it in build/dist.
def dist(context):
	print 'TODO: command `dist` is not yet implemented'


# Attempts to clone repository from remote index.
def fetch(context):
	if context.name.find('.git') >= 0:
		storage.fetch_unindexed_module(context.name)
	else:
		storage.fetch_module(context.name)


# Deletes module with given name from local index.
def remove(context):
	storage.clear_module(context.name)


# Sets up boilerplate project structure.
def init(context):
	os.makedirs('documentation')
	os.makedirs('sources')
	os.makedirs('tests')
	os.makedirs('documentation/generated')
	utility.touch('README.md')
	utility.touch('LICENSE.md')
	with open('sources/main.c', 'w') as f:
		f.write('''
			#include <stdio.h>

			int main()
			{
				printf("Hello, world!");
			}
			''')
	with open('tests/main.c', 'w') as f:
		f.write('''
			#include <stdio.h>

			int main()
			{
				printf("No tests to run.");
			}
			''')
	with open('.gitignore', 'w') as f:
		f.write('build\n')


# If building an application, its executable is made available 
# globally. Otherwise, the library is placed in the local index.
def install(context):
	build(None)
	name = os.path.abspath('.').split('/')[-1]
	if os.path.exists('sources/main.c'):
		shutil.copy('build/bin/' + name, '/usr/local/bin/' + name)
	else:
		dest = storage.module_path(name)
		shutil.copytree('.', dest)
		storage.index(name, 'none')


# Lists available modules (both local and remote).
def modules(context):
	local = storage.local_modules()
	remote = storage.remote_modules()
	print 'local:  (' + str(len(local)) + ')'
	for m in local:
		if storage.module_compiled(m[0]):
			print ' - ' + m[0], '[' + utility.color('compiled', 'green') + ']'
		else:
			print ' - ' + m[0], '[' + utility.color('not compiled', 'red') + ']'
	print '\nremote:  (' + str(len(remote)) + ')'
	for m in remote:
		print ' -', m[0], '[' + utility.color(m[1], 'yellow') + ']'


# Builds and runs generated executable.
def run(context):
	build(None)
	name = os.getcwd().split('/')[-1]
	os.execv('build/bin/' + name, context.args)


# Builds target and runs its tests.
def test(context):
	build(None)
	os.execv('build/bin/tests', [''])


# Hack.
def execute(context):
	globals()[context.command](context)