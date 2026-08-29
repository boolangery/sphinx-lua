# Prevent spurious errors during `python setup.py test` in 2.6, a la
# http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html:
try:
    import multiprocessing
except ImportError:
    pass

from io import open
from setuptools import setup, find_packages

ver_dic = {}
version_file = open("sphinx_lua/version.py")
try:
    version_file_contents = version_file.read()
finally:
    version_file.close()

exec(compile(version_file_contents, "sphinx_lua/version.py", 'exec'), ver_dic)

setup(
    name='sphinx-lua',
    version=ver_dic["__version__"],
    description='Support for using Sphinx on Luadoc-documented Lua code',
    long_description=open('README.rst', 'r', encoding='utf8').read(),
    author='Eliott Dumeix',
    author_email='eliott.dumeix@gmail.com',
    license='MIT',
    license_files=('LICENSE.txt',),
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    install_requires=[
        'Jinja2>3.0',
        'luadoc>=1.4.1',
        'sphinxcontrib-luadomain>=1.2.0'
    ],
    extras_require={
        'test': ['pytest', 'Sphinx'],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Software Development :: Documentation'
    ],
    python_requires='>=3.9',
    keywords=['sphinx', 'documentation', 'docs', 'lua', 'luadoc', 'restructured'],
)
