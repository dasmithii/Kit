import os
import shutil
import utility
import storage
import builder


def build(context):
	builder.build_directory('.')

def dist(context):
	print 'TODO'

def fetch(context):
	storage.fetch_module(context.name)

def remove(context):
	storage.clear_module(context.name)

def init(context):
	print 'TODO'

def install(context):
	build()
	for path in utility.files_under('build/bin'):
		shutil.copyfile(path, '/usr/local/bin')

def modules(context):
	local = storage.local_modules()
	remote = storage.remote_modules()
	print 'local:  (' + str(len(local)) + ')'
	for m in local:
		print ' - [' + m[0] + ']', m[1]
	print '\ncentral index:  (' + str(len(remote)) + ')'
	for m in remote:
		print ' - [' + m[0] + ']', m[1]

def register(context):
	print 'TODO'

def run(context):
	build()
	name = os.getcwd().split('/')[-1]
	os.execv('build/bin/' + name, context.args)

def execute(context):
	globals()[context.command](context)