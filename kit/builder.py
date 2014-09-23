import os
import shutil
import storage
import scanner
import utility


# Copies headers in module to build/headers/name, dropping one
# directory layer (i.e. name/sources/header.h => name/header.h)
# TODO: minimize headers
def prepare_headers(name):
    root = storage.module_path(name)
    baseheaders = root + '/build/headers/kit'
    headers = baseheaders + '/' + name
    for path in utility.headers_under(root):
        # don't duplicate if already prepared
        if path.find('build') == 0:
            continue

        # move file
        dest = path.replace(root + '/', '')
        dest = '/'.join(dest.split('/')[1:])
        if not os.path.exists(headers):
            os.makedirs(headers)
        shutil.copy(path, headers + '/' + dest)

        # make `#include <kit/name.h>` function as `#include <kit/name/{api.h,
        # name.h}>`
        short = path.replace(root + '/sources/', '')
        if short in ['api.h', 'api.hh', name + '.h', name + '.hh']:
            shutil.copy(
                path, baseheaders + '/' + name + short[short.find('.'):])
    print ' - prepared headers'


# Ensure that module is compiled.
def ready_indexed_module(name):
    if not storage.module_compiled(name):
        path = storage.module_path(name)
        build_directory(path)
        prepare_headers(name)
        print utility.color(' - compiled module: ' + name, 'green')


# Generates CMakeLists file for project. This should be removed after
# compilation.
def generate_cmake(root, deps):
    name = os.path.abspath(root).split('/')[-1]
    meta = scanner.directory_metadata(root)
    with open(root + '/CMakeLists.txt', 'w') as f:
        f.write('project(KitModule ' + meta['language'] + ')\n')
        f.write('cmake_minimum_required(VERSION 2.6)\n')
        f.write('cmake_policy(VERSION 2.6)\n')
        f.write(
            'set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)\n')
        f.write(
            'set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)\n')
        f.write(
            'set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)\n')
        if meta['language'] == 'C':
            f.write('SET(CMAKE_C_FLAGS  "' + meta['flags'] + '")\n')
        else:
            f.write('SET(CMAKE_CXX_FLAGS  "' + meta['flags'] + '")\n')

        # Fetch necessary files.
        headers = []  # reduce(operator.add, map(storage.header_paths, deps))
        sources = utility.sources_under(root + '/sources')
        test_sources = utility.sources_under(root + '/tests')

        # Build application [if sources/main.c is present].
        if scanner.has_main(root):
            files = sources + headers
            f.write(
                'add_executable(' + name + ' "' + '" "'.join(files) + '")\n')

        # Build module as static library.
        files = filter(lambda s: s.find('main.') == -1, headers + sources)
        if len(files) > 0:
            f.write(
                'add_library(' + name + '_static STATIC "' + '" "'.join(files) + '")\n')
            # f.write('set_target_properties(' + name + '_static PROPERTIES LINKER_LANGUAGE C)\n')

        # Build test executable.
        files += test_sources
        f.write('add_executable(tests "' + '" "'.join(files) + '")\n')

        # Link against compiled dendencies.
        for dep in deps:
            f.write('add_library(' + dep + ' STATIC IMPORTED)\n')
            f.write(
                'set_target_properties(' + dep + ' PROPERTIES IMPORTED_LOCATION "' + storage.module_library_path(dep) + '")\n')
            f.write('TARGET_LINK_LIBRARIES(tests ' + dep + ')\n')
            if scanner.has_main(root):
                f.write('TARGET_LINK_LIBRARIES(' + name + ' ' + dep + ')\n')
            f.write('include_directories(' + storage.module_header_path(dep) + ')\n')
    print ' - generated CMakeLists.txt'


# Performs any commands specified in the metadata file.
def run_configuration(path):
    meta = scanner.directory_metadata(path)
    for command in meta['commands']:
        os.system(command)



# Compiles executables and libraries for given project, assuming
# that all dependencies have been resolved a priori.
def make(path,options):
    print ' - running `make`...'
    wd = os.getcwd()
    os.chdir(path)
    run_configuration(path)
    os.system('mkdir -p build')
    os.chdir('build')
    c1 = os.system('cmake -Wno-dev .. > /dev/null')
    if options["verbose"]:
        c2 = os.system('make VERBOSE=1')
    else:
        c2 = os.system('make > /dev/null')
    if not options["save-cmake"]:
        os.system('rm ../CMakeLists.txt')
    os.chdir(wd)
    if c1 == 0 and c2 == 0:
        print utility.color(' - build successfull', 'green')
    else:
        print utility.color(' - build failed', 'red')
        exit(1)


# Compiles libraries and headers for given directory.
def build_directory(path,options):
    deps = scanner.recursive_dependencies(path)
    for dep in deps:
        # print ' - resolving dependency:', dep
        if not storage.contains_module(dep):
            if storage.remote_contains_module(dep):
                storage.fetch_module(dep)
            else:
                print utility.color(' - module not found: ' + dep, 'red')
                print utility.color(' - build failed', 'red')
                exit(1)
        ready_indexed_module(dep)
    generate_cmake(path, deps)
    make(path,options)
