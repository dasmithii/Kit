## Status
Not ready for primetime, but it's getting there.




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
1. Set a project.
    ```
    mkdir my-project
    cd my-project
    kit init
    ```
    At this point, [valid] boilerplate code has been generated, and `kit build`     will output two executables in build/bin: (1) the main application, and (2)     the unit test wrapper.

    + `kit run` is a shortcut for `./build/bin/my-project
    + `kit test` is a shortcut for `./build/bin/tests

2. Include modules from the centralized index.
    
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
    
3. Create your own modules.
    
    After developing a library, you may want access to it from other projects. To do locally, run `kit install-as <module-name>'. Then your code will be available in the same way `kit/base/vector.h` was above.

    Kit also maintains a central index, which anyone can access remotely. If you feel that your code could be useful to others, send a pull request with edits to MODULES.csv.

4. Distribute libraries & applications.
    
    Kit is capable of generating self-contained projects [which do not require kit itself]. These are beneficial, especially since the majority of C developers are unaware of kit.

    Run `kit dist` to do this. Output is directed to `build/dist`.





## Further Information
- [contributing](documentation/contributing.md)
- [tutorial](documentation/tutorial.md)