from distutils.core import setup

setup(
    name='filterbank',
    version='0.1.0',
    author='Ben Jeffery',
    author_email='ben.jeffery@well.ox.ac.uk',
    packages=['filterbank',],
    scripts=['scripts/filterbank'],
    license='LICENSE.TXT',
    url="http://github.com/malariagen/filterbank",
    description="Generate datasets at multiple resolutions",
    long_description=open('README.md').read(),
    install_requires=['pyyaml',]
)