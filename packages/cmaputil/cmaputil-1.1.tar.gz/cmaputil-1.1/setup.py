from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE.txt') as f:
    license = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

pkgs = find_packages(exclude=('examples'))

setup(
    name='cmaputil',
    version='1.1',
    description='Colormap analysis module',
    long_description=readme,
    author='Jamie R. Nunez',
    author_email='jamie.nunez@pnnl.gov',
    url='https://github.com/pnnl/cmaputil',
    license=license,
    packages=pkgs,
    install_requires=required
)
