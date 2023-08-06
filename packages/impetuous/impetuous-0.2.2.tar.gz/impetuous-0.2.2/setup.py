"""
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
# To use a consistent encoding
from codecs import open
from os import path


# https://stackoverflow.com/questions/40051076/babel-compile-translation-files-when-calling-setup-py-install

def do_bable_stuff(distribution):
    from babel.messages.frontend import compile_catalog
    compiler = compile_catalog(distribution)
    option_dict = distribution.get_option_dict('compile_catalog')
    print(option_dict)
    compiler.domain = [option_dict['domain'][1]]
    compiler.directory = option_dict['directory'][1]
    compiler.run()


class InstallWithCompile(install):

    def run(self):
        do_bable_stuff(self.distribution)
        super().run()


class DevelopWithCompile(develop):

    def run(self):
        do_bable_stuff(self.distribution)
        super().run()


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='impetuous',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.2.2',

    description='CLI time tracking software indented for use with JIRA',
    long_description=long_description,

    # The project's main homepage.
    url='https://gitlab.com/sqwishy/impetuous',

    # Author details
    author='sqwishy',
    author_email='somebody@froghat.ca',

    # Choose your license
    license='GPLv3',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Office/Business',
        'Topic :: Utilities',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',
    ],

    # What does your project relate to?
    keywords='todo',

    #cmdclass={
    #    'install': InstallWithCompile,
    #    'develop': DevelopWithCompile,
    #},

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['impetuous'],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['colorama', 'python-dateutil>=2.6.0', 'pyyaml', 'pytz', 'attrs'],

    setup_requires=['Babel'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'jira': ['aiohttp'],
        'freshdesk': ['aiohttp'],
        #'dev': ['check-manifest'],
        #'test': ['coverage'],
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={},
    #package_data={'': ['locale/*/*/*.mo', 'locale/*/*/*.po']},

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'im=impetuous.__main__:main',
        ],
    },
)
