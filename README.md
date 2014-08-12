## Overview
In contrast with many modern languages, C has no central authority of project management. From basic directory structure to build tools, everything seems fragmented. More so, libraries are inaccessibly scattered across the web - and that pressures developers to reinvent the wheel over and over again.

Kit is a solution to these problems. It provides standardized project structure, centralized module indexing, and a convenient build tool [which wraps CMake, capitalizing on standardization].



## Installation
```
git clone https://github.com/dasmithii/Kit.git
cd Kit
python setup.py install
cd ..
```



## Sample Usage
+ Set a project.
    ```
    mkdir my-project
    cd my-project
    kit init
    ```
    At this point, [valid] boilerplate code has been generated, and `kit build`     will output two executables in build/bin: (1) the main application, and (2)     the unit test wrapper.

    + `kit run` is a shortcut for `./build/bin/my-project
    + `kit test` is a shortcut for `./build/bin/tests

+ Include modules from the centralized index.
    
    ```
    // file: sources/main.c
    #include <kit/base/vector.h>

    int main() {
        vector vec;
        vector_init(&vec);
        // use vector here...
        vector_clean();
    }
    ```
    Kit recognizes `#include <kit/base*` and searches for a module named "base". If not installed already, it is downloaded from the central index and compiled as a static archive. Then, during `kit build`, the library is linked against and its headers added to the include path.
    
+ Create your own modules.
    
    To make code available in the same way `kit/base/vector.h` was above, run `kit install-as <module-name>'.

    If you feel that your code could be useful to others, send a pull request with edits to MODULES.csv. That file lists items in the central index.





## Further Information
- [contributing](documentation/contributing.md)
- [tutorial](documentation/tutorial.md)