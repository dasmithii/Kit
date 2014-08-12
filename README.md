## Status
Not ready for primetime, but it's getting there.




## Overview
In contrast with many modern languages, C has no central authority of project management. From basic directory structure to build tools, everything seems fragmented. More so, libraries are inaccessibly scattered across the web - and that pressures developers to reinvent the wheel over and over again.

Kit is a solution to these problems. It provides standardized project structure, centralized module indexing, and a convenient build tool [which wraps CMake, capitalizing on standardization].



## Sample Usage
Setup a project named my-project.
```
mkdir my-project
cd my-project
kit init
```
At this point, [valid] boilerplate code has been generated, and you may build the project with `kit build`. This will output two executables to build/bin: (1) the main application, and (2) the unit test wrapper.

+ `kit run` is a shortcut for `./build/bin/my-project
+ `kit test` is a shortcut for `./build/bin/tests





## Installation
```
git clone https://github.com/dasmithii/Kit.git
cd Kit
python setup.py install
cd ..
```



## Further Information
- [contributing](documentation/contributing.md)
- [tutorial](documentation/tutorial.md)