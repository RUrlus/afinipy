from __future__ import absolute_import

import os

from afinipy.exceptions import DirectoryNotFound


def path_list(path):
    """The path to the directory split on os.path.sep

    Parameters
    ----------
    path : str
        Path to directory

    Returns:
    list
        list of names of the directories in the path
    """
    return path.split(os.path.sep)


def dir_depth(path, base_depth=None):
    """The number of directories below the system root. If base_depth
    is passed the relative directory level is returned

    Parameters
    ----------
    path : str
        Path to directory
    base_depth : int/float
        The dir_depth of the relative root

    Returns:
    int
        the absolute or relative dir level
    """
    if isinstance(base_depth, (int, float)):
        return len(path.split(os.path.sep)) - base_depth
    else:
        return len(path.split(os.path.sep))


def dir_name(path):
    """Get name of the directory

    Parameters
    ----------
    path : str
        Path to directory

    Returns
    -------
    str
        The name of the directory
    """
    return os.path.split(path)[-1]


def adir(path):
    """Get full path to dir

    Parameters
    ----------
    path : str
        Path to directory

    Returns
    -------
    str
        The absolute path to dir

    Raises
    ------
    DirectoryNotFound
        If the path does not exist
    """
    apath = os.path.abspath(path)
    if not os.path.isdir(apath):
        raise DirectoryNotFound(path)
    return apath


def wdir():
    """Get absolute path to working directory

    Returns
    -------
    str
        abs path to working directory
    """
    return os.getcwd()


def mdir():
    """Get absolute path to module/notebook directory

    Returns
    -------
    str
        abs path to dir where file is located
    """
    try:
        p = os.path.realpath(os.path.dirname(__main__))
    except NameError:
        p = os.path.realpath(os.path.dirname('__main__'))
    return p


def pdir():
    """Get absolute path to parent directory

    Returns
    -------
    str
        abs path to parent directory
    """
    return os.path.realpath(os.path.pardir)


def sdir(dirname, filename=None):
    """Get path to sibling directory of name `dirname`

    Parameters
    ----------
    dirname : str | tuple | list
        The name of the sibling directory
    filename : str
        The name of the file in the sibling directory

    Returns
    -------
    str
        path to sibling directory or file
    """
    if isinstance(dirname, (tuple, list)):
        dirname = os.path.join(*dirname)
    if filename:
        return os.path.join(pdir(), dirname, filename)
    else:
        return os.path.join(pdir(), dirname)
