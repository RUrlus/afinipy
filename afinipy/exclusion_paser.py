from __future__ import absolute_import

import os

from afinipy.exceptions import FileNotFound


class ExclusionPaser(object):
    """Class that orchastrates the parsing of the exlusion path"""
    def __init__(self, path):
        """Initialise the class

        Parameters
        ----------
        path : str
            The absolute path to the module includign extension
        """
        # absolute path to module with extension
        self.path = os.path.realpath(path)

        if not os.path.isfile(self.path):
            raise FileNotFound(self.path)

        # Track empty lines
        self.empty_lines = []
        # Initialise line store
        self.line_store = {}
        # Initialise the module store
        self.module_store = set()
        # Initialise the module store
        self.udef_store = set()
        # Initialise the module store
        self.direc_store = set()

        self.uvars = ['udef', 'udefs', 'Udef', 'Udefs']
        self.mvars = ['module', 'modules', 'Module', 'Modules']
        self.dvars = ['directories', 'Directories', 'Dirs',
                      'dirs', 'direcs', 'Direcs', 'direc', 'Direc']

    def exclusion_parser(self):
        """Parse the exclusion file"""
        with open(self.path) as f:
            self.contents = [l.rstrip('\n') for l in f]
        self._parse_lines()
        return {
            'direc': self.direc_store,
            'module': self.module_store,
            'udef': self.udef_store
        }

    def _parse_lines(self):
        """Parse lines and create udef, module and directory store"""
        for i, line in enumerate(self.contents):
            if line == '':
                self.empty_lines.append(i)
            else:
                self.line_store[i] = line
                self.search_keyswords(self.uvars, self.udef_store)
                self.search_keyswords(self.mvars, self.module_store)
                self.search_keyswords(self.dvars, self.direc_store)

    def search_keyswords(self, options, store):
        """Search for keywoards in the lines and add to the respective store"""
        for number, line in self.line_store.items():
            for kw in options:
                defin, content = line.split(':')
                if kw == defin:
                    for k in content.split(','):
                        store.add(k.strip())
