from distutils.core import setup

with open('LICENSE') as file:
    license = file.read()

with open('README.rst') as file:
    long_description = file.read()

setup(
    name='testimony',
    version='1.0.6',
    url='https://github.com/SatelliteQE/testimony/',
    author='Suresh Thirugn',
    author_email='sthirugn@redhat.com',
    packages=['testimony'],
    scripts=['bin/testimony'],
    description='Testimony inspects and reports on the python test cases.',
    long_description=long_description,
    license=license,
)
