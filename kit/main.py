import sys
import commands
import utility


usage = '''
	Kit, a project manager for C/C++
	--------------------------------

	- usage:
	          kit <command> [all|<module>] [flags/options]

	- commands:
	          build ...... compile all sources
	          clean ...... remove compilation products
	          dist ....... generate kit-independent project
	          fetch ...... fetch from central or remote repository
	          help ....... get more information
	          remove ..... uninstall module
	          init ....... prepare new project
	          install .... make available globally
	          modules .... list available modules
	          run ........ execute outputted application
	          test ....... execute unit tests
'''


def run_cli():
	args = sys.argv
	if len(args) < 2:
		print utility.color(' - invalid argument list', 'red')
	else:
		com = args[1]
		arg = args[2] if len(args) > 2 else None
		if com == 'help':
			print usage
		else:
			commands.execute(com, arg) 


if __name__ == '__main__':
	run_cli()