# AF*ini*Py -- Automated filling of `__init__.py`
[![Travis CI](https://travis-ci.com/RUrlus/afinipy.svg?branch=master)](https://travis-ci.com/RUrlus/afinipy)

**Version:** 0.1.5

**Date:** 20-07-2019

**Author:** Ralph Urlus

Afinipy is a, CLI, python package that builds your init files for you.
It works by, recursively, parsing the directory and modules using Python's Abstract Syntax Trees.
Afinipy features two modes, top-level and recursive. The top-level mode builds a single `__init__` at
the root directory even if modules are located into subdirectories. The recursive mode will build a
`__init__` for each subdirectory. For additional options see the usage section below or the notebook
in the examples directory.

All 'private' functions, those starting with an underscore, are excluded from the init. Optionally,
additional functions, classes or the contents of a directory can be excluded by specifying them in
a file and passed to the `exclusion_path` parameter. See the exclusion path section below for details.
All functions or all classes can be excluded by, respectively, specifying `--exclude 'functions'` or `--exclude 'classes'`

## Installation
Install afinipy from PyPi
```shell
$ pip install afinipy
```
Install afinipy from Github with:
```shell
$ pip3 install git+https://github.com/RUrlus/afinipy
```
or clone the repository first
```shell
$ git clone https://github.com/RUrlus/afinipy.git
$ pip3 install afinipy/.
```

## Usage & Examples
Afinipy can be used from the command line or from python.
Assuming you are in the parent directory of the package or the directory containing the modules of interest. For example the `examples` directory in this 
```shell
$ afinipy top_level_example --mode top_level --dry_run
```

Alternatively from a python interpreter or notebook
```python3
from afinipy import Afinipy
root = 'examples/recursive_example'
inib = Afinipy(root, package='example', mode='recursive', exclusion_path='.exclude')
inib.build_init(dry_run=True)
```

### Exclusion path
The exclusion file is parsed expecting a particular syntax, the examples directory contains an example named `.exclude`.
The to be excluded directories, modules and user defined objects should be defined by specifying:
* `direcs:` for directories followed by the directory name, not the path.
* `modules:` for modules followed by the module name without the extension.
* `udefs:` for user defined functions and classes

If more than one exclusion is given for a specific type, e.g. udefs, they should be separated by a comma and on the same line.
The exclusion types should be on individual lines. 
```
direcs: <dir_name>

modules: <module_name>

udefs: <function_name>, <another function_name>
```

## License
- **[GNU license](https://opensource.org/licenses/GPL-3.0)**
- Copyright 2019 @ Ralph Urlus
