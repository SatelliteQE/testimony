from distutils.core import setup

setup(
    name='testimony',
    version='0.1dev',
    packages=['testimony',],
    scripts=['bin/testimony'],
    long_description=open('README.md').read(),
)
