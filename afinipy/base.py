from __future__ import absolute_import

import os

import afinipy.path_funcs as pf
import afinipy.utils as uf

from afinipy.directory import Directory
from afinipy.base_class import BaseClass
from afinipy.exclusion_paser import ExclusionPaser

from afinipy.exceptions import IllegalSetting
from afinipy.exceptions import WrongSettingsType


class Afinipy(BaseClass):
    """Base class that orchastrates the parsing and creation of
    the __init__ file.
    """
    def __init__(self, path, **kwargs):
        """Initialise the class.

        Parameters
        ----------
        path : str
            The path to the root of the directory
        mode : str
            The mode to run afinipy in. Options are:
            - top_level: everything is set in top level __init__
            - recursive: each directory level gets own __init__
            Optional, default is `top_level`
        package : str
            Package name; default is `None`
        exclude : str, optional
            Exclude all functions or classes
        exclusion_path : str, optional
            Path to the file containing the exclusions
        verbose : bool
            Print the import statements
        dry_run : bool
            Do not write the __init__ but only print

        """
        # validate type and value of parameters
        if not isinstance(path, str):
            raise WrongSettingsType('path', path, str)

        # get absolute path and check existence
        self._base_path = pf.adir(path)

        # The way to build the inits
        self._mode = kwargs.pop('mode', 'top_level')

        # validate mode setting
        if (
            (self._mode is not None) and
            (self._mode not in {'top_level', 'recursive'})
        ):
            raise IllegalSetting('mode', self._mode)

        # The prefix for the import statements
        self._package = kwargs.pop('package', '')

        self.exclude = kwargs.pop('exclude', None)

        self._verbose = kwargs.pop('verbose', False)
        self._dry_run = kwargs.pop('dry_run', False)

        # exclusion_path to the directories the user wants excluded
        self.exclusion_path = kwargs.pop('exclusion_path', None)

        if self.exclusion_path:
            ep = ExclusionPaser(self.exclusion_path)
            exclusions = ep.exclusion_parser()

            self._dir_exclude = exclusions['direc']
            self._module_exclude = exclusions['module']
            self._udef_exclude = exclusions['udef']
        else:
            self._dir_exclude = set()
            self._module_exclude = set()
            self._udef_exclude = set()

        self._name = pf.dir_name(self._base_path)

        # the number of directories we are from system root
        self._base_depth = pf.dir_depth(self._base_path)

        # list of the names of the directories from root
        self._base_path_list = pf.path_list(self._base_path)

        # initialise the directory collection where the target directory
        # is the root directory
        self.dirs = []

    def build_init(self, **kwargs):
        """Create the init file(s).

        Run the directory parser which will build inits per
        directory if mode is recursive else collect all statements
        and create the init

        Parameters
        ----------
        verbose : bool
            Print import statements; default is `False`
        dry_run : bool
            do not write, only print

        """
        self._verbose = self._verbose or kwargs.pop('verbose', False)

        self._dry_run = self._dry_run or kwargs.pop('dry_run', False)
        if self._dry_run:
            self._verbose = True

        # reset self.dirs to prevent extending
        self.dirs = []

        # start parsing
        self.directory_parser()

        if self._mode == 'top_level':
            self.top_level()
            if not self._dry_run:
                self.write_init()

    def _get_parents(self, path):
        """Get and concat parents to directory.

        Parameters
        ----------
        path : str
            The path to the directory

        Returns
        -------
        str
            The parents concatonated with seperator sep

        """
        return uf.concat_imports(
            (self._package, pf.path_list(path)[self._base_depth:])
        )

    def _exclude_dir(self, d):
        """Determine if the directory is relevant.

        Parameters
        ----------
        d : str
            the name of the directory

        Returns
        -------
        bool
            whether to exclude the directory

        """
        return (d[0] in {'_', '.'}) or (d in self._dir_exclude)

    def directory_parser(self):
        """Recursively search the target directory and create collection
        all directory classes with the python modules in that directory
        as attribute.
        """

        # Loop through all directories in and below base_path
        for root, dirs, files in os.walk(self._base_path):
            # extract the name of current directory
            dname = pf.dir_name(root)
            # check if directory should be excluded
            if self._exclude_dir(dname):
                continue
            else:
                self.dirs.append(
                    Directory(
                        path=root,
                        mode=self._mode,
                        package=self._package,
                        parents=self._get_parents(root),
                        files=files,
                        exclude=self._module_exclude,
                        cf_exclude=self.exclude,
                        udef_exclude=self._udef_exclude,
                        verbose=self._verbose,
                        dry_run=self._dry_run
                    )
                )

    def top_level(self):
        """Create __init__ at root level with all user defined functions
        and classes in the directory tree.
        """
        self.imports = []
        self.all_udefs = []
        for direc in self.dirs:
            for module in sorted(direc.modules, key=lambda x: x.name.lower()):
                self.all_udefs.extend(module.udefs)
                block = []
                for udef in sorted(module.udefs, key=lambda x: x.lower()):
                    # Template imports
                    block.append('from {0} import {1}\n'.format(
                        uf.concat_imports((module.parents, module.name)),
                        udef
                        )
                    )
                self.imports.append(''.join(block))
        self.imports = '\n'.join(self.imports) + '\n'
        if self._verbose:
            print('Import statements directory: ', self._name)
            print(self.imports)
            self._write_all()
