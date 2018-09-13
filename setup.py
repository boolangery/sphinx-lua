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
    version='1.0.1',
    description='Support for using Sphinx on Luadoc-documented Lua code',
    long_description=open('README.rst', 'r', encoding='utf8').read(),
    author='Eliott Dumeix',
    author_email='eliott.dumeix@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['ez_setup']),
    tests_require=['nose',
                   'recommonmark==0.4.0',
                   # Sphinx's plain-text renderer changes behavior slightly
                   # with regard to how it emits class names and em dashes from
                   # time to time:
                   'Sphinx==1.7.2'],
    test_suite='nose.collector',
    include_package_data=True,
    install_requires=[
        'Jinja2>2.0,<3.0',
        'Sphinx<2.0',
        'luadoc',
        'sphinxcontrib-luadomain==1.0.0'
        ],
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Software Development :: Documentation'
        ],
    keywords=['sphinx', 'documentation', 'docs', 'lua', 'luadoc', 'restructured'],
)
