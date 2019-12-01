from setuptools import setup, find_packages

LONG_DESCRIPTION = """
Afinipy is a, CLI, python package that builds your init files for you.
It works by, recursively, parsing the directory and modules using Python's Abstract Syntax Trees.
Afinipy features two modes, top-level and recursive. The top-level mode builds a single `__init__` at
the root directory even if modules are located into subdirectories. The recursive mode will build a
`__init__` for each subdirectory. For additional options see the usage section below or the notebook
in the examples directory.

All 'private' functions, those starting with an underscore, are excluded from the init. Optionally,
additional functions, classes or the contents of a directory can be excluded by specifying them in
a file and passed to the `exclusion_path` parameter.
All functions or all classes can be excluded by, respectively, specifying `--exclude 'functions'` or `--exclude 'classes'`

See https://github.com/RUrlus/afinipy for details
"""

setup(
    name='afinipy',
    version='0.2.0',
    description='Automated init builder',
    author='Ralph Urlus',
    author_email='rurlus.dev@gmail.com',
    packages=find_packages(exclude=('tests',)),
    long_description=LONG_DESCRIPTION,
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        afinipy=afinipy.afinipy:cli
    ''',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/RUrlus/afinipy/issues',
        'Source': 'https://github.com/RUrlus/afinipy',
    },
    keywords='init development',
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: BSD License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # These classifiers are *not* checked by 'pip install'. See instead
        # 'python_requires' below.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
