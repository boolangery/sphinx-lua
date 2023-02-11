# Prevent spurious errors during `python setup.py test` in 2.6, a la
# http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html:
try:
    import multiprocessing
except ImportError:
    pass

from io import open
from setuptools import setup, find_packages

setup(
    name='sphinx-lua',
    version='1.1.4',
    description='Support for using Sphinx on Luadoc-documented Lua code',
    long_description=open('README.rst', 'r', encoding='utf8').read(),
    author='Eliott Dumeix',
    author_email='eliott.dumeix@gmail.com',
    license='MIT',
    license_files=('LICENSE.txt',),
    packages=find_packages(exclude=['ez_setup']),
    test_suite='nose.collector',
    include_package_data=True,
    install_requires=[
        'six',
        'Jinja2>3.0',
        'luadoc>=1.3.0',
        'sphinxcontrib-luadomain>=1.1.1'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Software Development :: Documentation'
    ],
    keywords=['sphinx', 'documentation', 'docs', 'lua', 'luadoc', 'restructured'],
)
