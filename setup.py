from setuptools import setup, find_packages

setup(
    name='afinipy',
    version='0.1.3',
    description='Automated init builder',
    author='Ralph Urlus',
    author_email='rurlus.dev@gmail.com',
    packages=find_packages(exclude=('tests',)),
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        afinipy=afinipy.afinipy:cli
    ''',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',
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
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # These classifiers are *not* checked by 'pip install'. See instead
        # 'python_requires' below.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
