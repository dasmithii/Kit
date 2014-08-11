import sys
import argparse
import commands

parser = argparse.ArgumentParser()
subs = parser.add_subparsers(dest='command')

subs.add_parser('build', help='compile executable/library')
subs.add_parser('clean', help='erase build products')
subs.add_parser('dist', help='generate C project without dependencies on kit')
subs.add_parser('fetch', help='download module from central index').add_argument('name', action='store')
subs.add_parser('remove', help='deletes module from local index').add_argument('name', action='store')
subs.add_parser('init', help='initialize project structure')
subs.add_parser('install', help='install project globally')
subs.add_parser('modules', help='list available modules')
subs.add_parser('register', help='include project in system-wide directory')
subs.add_parser('run', help='compile and run executable')
subs.add_parser('test', help='run tests for given module, defaulting to current')



def run_cli():
	args = sys.argv[1:]
	context = parser.parse_args(args)
	if context.command == 'run':
		context.args = [sys.argv[0]] + args[1:]
	commands.execute(context)

if __name__ == '__main__':
	run_cli()