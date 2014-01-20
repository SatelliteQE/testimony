from distutils.core import setup

with open('README.rst') as file:
    long_description = file.read()

setup(
    name='testimony',
    version='0.1.0',
    url='https://github.com/sthirugn/testimony/',
    author='Suresh Thirugn',
    author_email='sthirugn@redhat.com',
    packages=['testimony'],
    scripts=['bin/testimony'],
    long_description=long_description,
)
