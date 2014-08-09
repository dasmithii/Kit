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
	headers = root + '/build/headers/kit' + name
	for path in utility.headers_under(root):
		if path.find('build') == 0:
			continue
		temp = path.replace(root + '/', '')
		temp = temp[temp.find('/'):]
		dest = headers + dest
		shutil.copyfile(path, dest)


# Ensures that module is compiled and ready to be included in other
# projects.
def ready_module(root):
	if not os.path.exists(root + '/' + 'build'):
		build_directory(root)
		prepare_headers(name)


# Same as above but for globally-available modules.
def ready_indexed_module(name):
	path = storage.module_path(name)
	ready_module(path)	


# Generates CMakeLists file for project. This should be removed after
# compilation.
def generate_cmake(path, refs):
	name = path.split('/')[-1]
	with open(path + '/CMakeLists.txt') as f
		f.write('project KitModule C\n')
		f.write('cmake_minimum_required (VERSION 2.6)\n')
		f.write('set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)\n')
		f.write('CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin\n')
		f.write('CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin\n')
		f.write('SET(CMAKE_C_FLAGS  "-g -Wall -O2")\n')
		f.write('file(GLOB_RECURSE sources "sources/*.c")\n')
		f.write('file(GLOB_RECURSE test_sources "tests/*.c")\n')
		if os.path.exists(path + '/sources/main.c\n'):
			f.write('add_executable(' + name + ' ${sources})\n')
			f.write('set(tests2 ${sources} ${test_sources})\n')
			f.write('list(REMOVE_ITEM test_sources2 ' + path + '/sources/main.c\n')
			f.write('add_executable(tests ${sources} ${test_sources2})\n')
		else:
			f.write('add_library(' + name + '_shared SHARED ${sources})\n')
			f.write('add_executable(tests ${sources} ${test_sources})\n')
		for ref in refs:
			f.write('add_library(' + ref + ' SHARED IMPORTED)\n'
			f.write('set_target_properties(' + ref + ' PROPERTIES IMPORTED_LOCATION ' + storage.module_path(ref) + ')\n')
			f.write('TARGET_LINK_LIBRARIES(' + name + ' ' + ref + ')\n')
			f.write('TARGET_LINK_LIBRARIES(' + name + '_shared ' + ref + ')\n')
			f.write('include_directories(' + storage.modules + '/' + ref + '/headers' + ')\n')



# Compiles executables and libraries for given project, assuming
# that all dependencies have been resolved a priori.
def make(path):
	wd = os.getcwd()
	os.chdir(path)
	os.system('mkdir -p build')
	os.chdir('build')
	os.system('cmake ..')
	os.system('make')
	os.system('rm ../CMakeLists.txt')
	os.chdir(wd)

	
# Compiles libraries and headers for given directory.
def build_directory(path):
	refs = scanner.directory_references(path)
	for name in refs:
		ready_module(name)
	generate_cmake(path, refs)
	make(path)

# Applies to current directory.
def build():
	build_directory('.')