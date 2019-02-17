import ast

from afinipy.exceptions import IllegalSetting


class Module(object):
    """Class that orchastrates the parsing of a module in
    the tree of the target directory
    """
    def __init__(self, name, path, parents, exclude=None):
        """Initialise the class

        Parameters
        ----------
        name : str
            The name of the module
        path : str
            The absolute path to the module includign extension
        parents : str
            The parent directories starting at the target path
        exclude : None, str
            Exclude classes or functions.
        """

        # name of the class is the module name
        self.name = name

        # absolute path to module with extension
        self.path = path

        # the name(s) of the parent directories seperated by a dot
        self.parents = parents

        # whether to exclude functions, classes
        self.exclude = exclude

        # module parser sets all the functions and classes found in
        # module and exclude those that are marked private
        self.module_parser()

    def _extract(self, v):
        """Determine is value should be extracted

        Parameters
        ----------
        v : ast.child_node

        Returns
        -------
        bool
            Whether the value should be extracted
        """
        return (isinstance(v, (ast.ClassDef, ast.FunctionDef)) and (v.name[0] != '_'))

    def _extract_classes(self, v):
        """Determine is value should be extracted

        Parameters
        ----------
        v : ast.child_node

        Returns
        -------
        bool
            Whether the value should be extracted
        """
        return (isinstance(v, ast.ClassDef) and (v.name[0] != '_'))

    def _extract_funcs(self, v):
        """Determine is value should be extracted

        Parameters
        ----------
        v : ast.child_node

        Returns
        -------
        bool
            Whether the value should be extracted
        """
        return (isinstance(v, ast.FunctionDef) and (v.name[0] != '_'))

    def module_parser(self):
        """Extract both classes and functions from module"""

        # parse the file and create a syntax tree
        with open(self.path) as fh:
            mroot = ast.parse(fh.read(), self.path)

        if self.exclude is None:
            # Extract both classes and functions from module, excluding
            # those that begin with `_`
            self.udefs = [n.name for n in ast.iter_child_nodes(mroot) if self._extract(n)]

        elif self.exclude == 'functions':
            # Extract classes from module, excluding
            # those that begin with `_`
            self.udefs = [n.name for n in ast.iter_child_nodes(mroot) if self._extract_classes(n)]

        elif self.exclude == 'classes':
            # Extract functions from module, excluding
            # those that begin with `_`
            self.udefs = [n.name for n in ast.iter_child_nodes(mroot) if self._extract_funcs(n)]

        else:
            raise IllegalSetting('udef_exclude', self.udef_exclude)
