## Installation
If you haven't already, please follow these steps. They will install `kit`, which is necessary for the remainder of this tutorial.
```
git clone https://github.com/dasmithii/Kit.git
cd Kit
python setup.py install
cd ..
```



## Project Creation
Kit manages everything but the writing of code, and it all begins with standardized project structure. Run `kit init` from an empty directory to generate boilerplate files.

By default, this creates a project with two targets: (1) the main executable, and (2) a unit test executable. These are compiled automatically with `kit build`. In the same fashion, a library is build if `sources/main.c` cannot be found. So, if you're developing a library, rather than an application, simply delete `main.c`.



## Package Management
