from distutils.core import setup

setup(
    name='testimony',
    version='0.1.0',
    url='https://github.com/sthirugn/testimony/',
    author='Suresh Thirugn',
    author_email='sthirugn@redhat.com',
    packages=['testimony', ],
    scripts=['bin/testimony'],
    long_description=open('README.md').read(),
)
