from setuptools import setup

setup(
    name='afinipy',
    version='0.1.0',
    description='Automated init builder',
    author='Ralph Urlus',
    author_email='rurlus.dev@gmail.com',
    packages=['afinipy'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        afinipy=afinipy.afinipy:cli
    ''',
)
