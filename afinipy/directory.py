import os
import sys

import afinipy.path_funcs as pf
from afinipy.module import Module


class Directory(object):
    """Class that orchastrates the parsing of a directory in
    the tree of the target directory
    """
    def __init__(self, path, level, parents, files, exclude=None, udef_exclude=None):
        """Initialise the class

        Parameters
        ----------
        path : str
            The path to the root of the directory
        level : int
            The level from the root directory
        parents : str
            The parent directories starting at the target path
        files : list
            The files in the directory
        exclude : list-like
            The modules to exclude
        udef_exclude : None, str
            Exclude `classes` or `functions`
        """
        # get absolute path and check existence
        self.root = pf.adir(path)

        # name of the class is the directory name
        self.name = pf.dir_name(self.root)

        # the name(s) of the parent directories seperated by a dot
        self.parents = parents

        # the level from the target directory
        self.level = level

        # files contains all files found
        # in the root directory
        self.files = files

        # the modules that should be excluded
        self.exclude = exclude or set()
        self.exclude.update({'__init__', 'setup'})

        self.udef_exclude = udef_exclude

        # files parser sets all the python modules found
        # in the directory and creates module objects for each
        self.files_parser()

    def _ismodule(self, f):
        """Check if file is python module

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
        self.module_names = set([os.path.splitext(f)[0] for f in self.files if self._ismodule(f)])

        # prepend the sys.path with the directory, this is has no
        # side-effects outside this interpreter process and would have
        # otherwise been done by pyclbr
        sys.path = [self.root] + sys.path

        self.modules = [
            Module(
                name=module,
                path=os.path.join(self.root, module) + '.py',
                parents=self.parents,
                exclude=self.udef_exclude)
            for module in self.module_names
        ]
