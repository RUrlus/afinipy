from __future__ import absolute_import

import click

from afinipy.base import Afinipy


@click.command()
@click.argument('path', type=click.Path(exists=True), required=True)
@click.option('--mode', '-m', default='top_level', help='Type of __init__(s) to build. Default is "top_level"')
@click.option('--package', '-P', default='', help='Name of the package the init will be build for')
@click.option('--exclude', '-e', default=None, help='Exclude all functions or classes')
@click.option('--exclusion_path', '-E', default=None, type=click.Path(exists=True),
              required=False, help='Path to exclusion file')
@click.option('--verbose', '-v', is_flag=True, default=False, help='Print import statements')
@click.option('--dry_run', is_flag=True, default=False, help='Do not write, only print')
def cli(path, mode, package, exclude, exclusion_path, verbose, dry_run):
    """Build __init__ file for the package

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
    # Obtain path to target directory
    afinipy = Afinipy(
        path,
        mode=mode,
        package=package,
        exclude=exclude,
        exclusion_path=exclusion_path,
        verbose=verbose,
        dry_run=dry_run
    )
    afinipy.build_init()


if __name__ == '__main__':
    cli()
