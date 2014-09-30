import sys
import commands
import utility


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


option_table = {
    'v': 'verbose',
    's': 'save-cmake',
    'd': 'debug'
}

def is_option(s):
    return s[:1] == '-'

def not_option(s):
    return not is_option(s)

def parse_option(a):
    if a[:2] == '--' and a[2:] in option_table.values():
        return a[2:]
    elif a[:1] == '-' and a[1:] in option_table.keys():
        return option_table[a[1:]]
    else:
        print utility.color(' - ERROR: invalid option: ' + a, 'red')
        quit()


def run_cli():
    argv = sys.argv[1:]
    args = filter(not_option, argv)
    opts = map(parse_option, filter(is_option, argv))
    com = args[0] if len(args) > 0 else 'run'
    arg = args[1] if len(args) > 1 else None

    if com == 'help':
        print usage
    else:
        try:
            commands.execute(com, arg, opts)
        except KeyboardInterrupt:
            print '\n[kit]: aborting due to keyboard interupt'


if __name__ == '__main__':
    run_cli()
