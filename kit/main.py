import sys
import commands
import utility
import argparse


usage = '''
	Kit, a project manager for C/C++
	--------------------------------

	- usage:
	          kit <command> [all|<module>] [flags/options]
	          kit [flags/options]

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


# Main interface.
def run_cli():
    parser = argparse.ArgumentParser(usage)
    parser.add_argument("--save-cmake",dest="save_cmake",action="store_true")
    parser.add_argument("--verbose",dest="verbose",action="store_true")
    parser.add_argument("args",nargs="+")
    args_and_options = parser.parse_args()
    args = args_and_options.args
    options = {"verbose":args_and_options.verbose,
               "save-cmake":args_and_options.save_cmake}

    if len(args) == 0:
    	args.append('run')
    com = args[0]
    arg = args[1] if len(args) > 1 else None
    if com == 'help':
        print usage
    else:
        try:
            commands.execute(com, arg,options)
        except KeyboardInterrupt:
            print '\n[kit]: aborting due to keyboard interupt'


if __name__ == '__main__':
    run_cli()
