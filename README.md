# AF*ini*Py -- Automated filling of __init__.py

**Version:** 0.1.0

**Date:**07-04-2019

**Author:** Ralph Urlus

Afinipy is a, CLI, python package that builds your init files for you.
It works by, recursively, parsing the directory and modules using Python's Abstract Syntax Trees.
Afinipy features two modes, top-level and recursive. The top-level mode builds a single __init__ at
the root directory even if modules are located into subdirectories. The recursive mode will build a
__init__ for each subdirectory. For additional options see the usage section below or the notebook
in the examples directory.

## Installation
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

## License
- **[GNU license](https://opensource.org/licenses/GPL-3.0)**
- Copyright 2019 @ Ralph Urlus
