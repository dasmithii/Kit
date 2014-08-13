# Overview
In contrast with many modern languages, C has no central authority of project management. From basic directory structure to build tools, everything seems fragmented. More so, libraries are inaccessibly scattered across the web - and that pressures developers to reinvent the wheel over and over again.

Kit is a solution to these problems. It provides standardized project structure, centralized module indexing, and a convenient build tool [which wraps CMake, capitalizing on standardization].



# Installation
```
git clone https://github.com/dasmithii/Kit.git
cd Kit
python setup.py install
cd ..
```



# Sample Usage
#### Spawn a boilerplate project.
```
mkdir my-project
cd my-project
kit init
```
+ `kit run` is short for `./build/bin/my-project`
+ `kit test` is short for `./build/bin/tests`

#### Include kit modules.
`kit build` scans the source tree for lines that match `#include <kit/*>`, attempting to resolve each dependency. This is done by searching the local index, and if specified modules aren't found, by resorting to the central registry. Located modules are linked against, and their corresponding headers are added to the include path.

tl;dr: to include a module, `#include <kit/module/file.h`.
    
#### Create kit modules.
    
To make code available locally, run `kit install'. If you feel that your code could be useful to others, send a pull request with edits to MODULES.csv. That file lists items in the central index.





# Further Information
- [contributing](documentation/contributing.md)
- [tutorial](documentation/tutorial.md)