import os
import shutil
import utility
import storage
import builder

def clean(context):
	shutil.rmtree('build', ignore_errors=True)

def build(context):
	builder.build_directory('.')


def dist(context):
	print 'TODO'


def fetch(context):
	storage.fetch_module(context.name)


def remove(context):
	storage.clear_module(context.name)


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


def install(context):
	build()
	if os.path.exists('sources/main.c'):
		name = os.path.abspath(path).split('/')[-1]
		shutil.copy('build/bin/' + name, '/usr/local/bin/' + context.name)
	else:
		dest = storage.module_path(context.name)
		shutil.copytree('.', dest)
		storage.index(context.name, '')


def modules(context):
	local = storage.local_modules()
	remote = storage.remote_modules()
	print 'local:  (' + str(len(local)) + ')'
	for m in local:
		if storage.module_compiled(m[0]):
			print ' - ' + m[0], '[' + utility.color('compiled', 'green') + ']'
		else:
			print ' - ' + m[0], '[' + utility.color('not compiled', 'red') + ']'
	print '\ncentral index:  (' + str(len(remote)) + ')'
	for m in remote:
		print ' -', m[0], '[' + utility.color(m[1], 'yellow') + ']'


def register(context):
	print 'TODO'


def run(context):
	build(None)
	name = os.getcwd().split('/')[-1]
	os.execv('build/bin/' + name, context.args)


def test(context):
	build(None)
	os.execv('build/bin/tests', [''])


def execute(context):
	globals()[context.command](context)