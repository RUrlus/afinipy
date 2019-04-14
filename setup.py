from setuptools import setup, find_packages

setup(
    name='afinipy',
    version='0.1.2',
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
)
