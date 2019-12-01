from __future__ import absolute_import

import os

import afinipy.utils as uf
import afinipy.path_funcs as pf

from afinipy.module import Module
from afinipy.base_class import BaseClass


class Directory(BaseClass):
    """Class that orchastrates the parsing of a directory in
    the tree of the target directory
    """
    def __init__(
        self, path, mode, package, parents, files, exclude=None,
        cf_exclude=None, udef_exclude=None, verbose=False, dry_run=False
    ):
        """Initialise the class.

        Parameters
        ----------
        path : str
            The path to the root of the directory
        mode : str
            top_level or recursive
        package : str
            the prefix for the import statement ['.', 'package_name']
        parents : str
            The parent directories starting at the target path
        files : list
            The files in the directory
        exclude : list-like
            The modules to exclude
        cf_exclude : str, None
            Exclude `classes` or `functions`
        udef_exclude : set
            Set of functions or classes to be excluded
        verbose : bool
            Print the import statements
        dry_run : bool
            do not write, only print

        """
        # get absolute path and check existence
        self.root = pf.adir(path)
        self._base_path = self.root

        # top_level or recursive
        self.mode = mode

        # the prefix for the print statements
        self.package = package

        # name of the class is the directory name
        self.name = pf.dir_name(self.root)

        # the name(s) of the parent directories seperated by a dot
        self.parents = parents

        # files contains all files found
        # in the root directory
        self.files = files

        # the modules that should be excluded
        self.exclude = exclude or set()
        self.exclude.update({'__init__', 'setup'})

        self.cf_exclude = cf_exclude
        self.udef_exclude = udef_exclude

        # print import blocks
        self.verbose = verbose

        # Don't write only print
        self.dry_run = dry_run
        if self.dry_run:
            self.verbose = True

        # files parser sets all the python modules found
        # in the directory and creates module objects for each
        self.files_parser()

        if self.mode == 'recursive':
            self.build_init()
            if not self.dry_run:
                self.write_init()

    def _ismodule(self, f):
        """Check if file is python module.

        Parameters
        ----------
        f : str
            path to file

        Returns
        -------
        bool
            whether the file is a python module that is relevant
        """
        if os.path.isfile(os.path.join(self.root, f)):
            name, ext = os.path.splitext(f)
            return ((ext == '.py') and
                    (name[0] not in {'.', '_'}) and
                    (name not in (self.exclude)))
        else:
            return False

    def files_parser(self):
        """Filter the python modules from the files and set as modules,
        where we exclude dotfiles, files starting with `_` and
        __init__ files.

        For each module we create a Module instance that extracts the
        functions and classes without importing and correcting for
        star imports in the module
        """
        # create the list of module names
        self.module_names = set([
            os.path.splitext(f)[0] for f in self.files if self._ismodule(f)
        ])

        self.modules = [
            Module(
                name=module,
                path=os.path.join(self.root, module) + '.py',
                parents=self.parents,
                exclude=self.cf_exclude,
                udef_exclude=self.udef_exclude)
            for module in self.module_names
        ]

    def build_init(self):
        """Collect udefs from modules and create all_udefs and imports.

        We create a string that contains the import statements sorted
        alphabetically per module and within modules. A module's
        statements are seperated by a newline
        """
        # if recursive and no package is given we strip the parents
        if self.package == '':
            self.parents = ''

        self.imports = []
        self.all_udefs = []
        for module in sorted(self.modules, key=lambda x: x.name.lower()):
            block = []

            # collect all the udefs for __all__
            self.all_udefs.extend(module.udefs)

            for udef in sorted(module.udefs, key=lambda x: x.lower()):
                # Template imports
                block.append('from {0} import {1}\n'.format(
                    uf.concat_imports((self.parents, module.name)), udef
                ))
            # create block of import statements per module seperated
            # by empty line
            self.imports.append(''.join(block))
        self.imports = '\n'.join(self.imports)
        if self.verbose:
            print('Import statements directory: ', self.name)
            print(self.imports)
            self._write_all()
