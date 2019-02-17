import os

import afinipy.path_funcs as pf
import afinipy.utils as uf

from afinipy.directory import Directory

from afinipy.exceptions import IllegalSetting
from afinipy.exceptions import WrongSettingsType


class Afinipy(object):
    """Base class that orchastrates the parsing and creation of
    the __init__ file
    """
    def __init__(
            self,
            path,
            mode=None,
            dir_exclude=None,
            module_exclude=None):
        """Initialise the class

        Parameters
        ----------
        path : str
            The path to the root of the directory
        mode : str
            The mode to run afinipy in. Options are:
            - top_level: everything is set in top level __init__
            - recursive: each directory level gets own __init__
        dir_exclude : list-like
            The directories to exclude
        module_exclude : list-like
            The modules to exclude
        """
        # validate type and value of parameters
        if not isinstance(path, str):
            raise WrongSettingsType('path', path, str)

        if (mode is not None) and (mode not in {'top_level', 'recursive'}):
            raise IllegalSetting('mode', mode)

        # The way to build the inits
        self._mode = mode or 'top_level'

        # get absolute path and check existence
        self._base_path = pf.adir(path)

        # the number of directories we are from system root
        self._base_depth = pf.dir_depth(self._base_path)

        # list of the names of the directories from root
        self._base_path_list = pf.path_list(self._base_path)

        self._dir_exclude = dir_exclude or set()

        self._module_exclude = module_exclude or set()

        # initialise the directory collection where the target directory
        # is the root directory
        self.dirs = []

    def build_init(self):
        self.directory_parser()
        self.top_level()

    def _get_parents(self, path):
        """Get and concat parents to directory

        Parameters
        ----------
        path : str
            The path to the directory

        Returns
        -------
        str
            The parents concatonated with seperator sep
        """
        return uf.concat_strings(uf.ordered_notin(pf.path_list(os.path.split(path)[0]), self._base_path_list))

    def _exclude_dir(self, d):
        """Determine if the directory is relevant

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
        as attribute
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
                        level=pf.dir_depth(root, self._base_depth),
                        parents=self._get_parents(root),
                        files=files,
                        exclude=self._module_exclude
                    )
                )

    def top_level(self):
        """Create __init__ at root level with all user defined functions
        and classes in the directory tree
        """
        secondary_line = False
        all_udefs = []
        with open(os.path.join(self._base_path, '__init__.py'), 'w+') as init_file:
            # Write the __init__, create if it doesn't exist
            for direc in self.dirs:
                for module in sorted(direc.modules, key=lambda x: x.name.lower()):
                    all_udefs.extend(module.udefs)
                    if secondary_line:
                        init_file.write('\n')
                    else:
                        secondary_line = True
                    for udef in sorted(module.udefs, key=lambda x: x.lower()):
                        # Template imports
                        init_file.write('from .{0}{1} import {2}\n'.format(module.parents, module.name, udef))

            # The objects that will be added for __all__
            # Template for __all__ functions in all modules
            init_file.write('\n__all__ = {}\n'.format(sorted(all_udefs, key=lambda x: x.lower())))
        init_file.close()
        print('{} has been appended/generated'.format(os.path.join(self._base_path, '__init__.py')))
