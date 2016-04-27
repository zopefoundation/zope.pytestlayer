"""Integration of zope.testrunner-style test layers into py.test framework"""

from setuptools import setup, find_packages
import glob
import os.path


def project_path(*names):
    """Get a path."""
    return os.path.join(os.path.dirname(__file__), *names)


setup(
    name='gocept.pytestlayer',
    version='4.0',

    install_requires=[
        'pytest',
        'setuptools',
        'six',
        'zope.dottedname',
    ],

    extras_require={
        'test': [
            'plone.testing',
        ],
    },

    entry_points={
        'console_scripts': [
            # 'binary-name = gocept.pytestlayer.module:function'
        ],
        'pytest11': [
            'zopelayer = gocept.pytestlayer.plugin',
        ],
    },

    author='gocept <mail@gocept.com>',
    author_email='mail@gocept.com',
    license='ZPL 2.1',
    url='https://bitbucket.org/gocept/gocept.pytestlayer/',

    keywords='',
    classifiers="""\
Development Status :: 4 - Beta
Environment :: Console
Framework :: Plone
Framework :: Zope2
Framework :: Zope3
Intended Audience :: Developers
License :: OSI Approved
License :: OSI Approved :: Zope Public License
Natural Language :: English
Operating System :: OS Independent
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.5
Programming Language :: Python :: Implementation
Programming Language :: Python :: Implementation :: CPython
Programming Language :: Python :: Implementation :: PyPy
Topic :: Software Development
Topic :: Software Development :: Libraries
Topic :: Software Development :: Libraries :: Python Modules
Topic :: Software Development :: Testing
"""[:-1].split('\n'),
    description=__doc__.strip(),
    long_description='\n\n'.join(open(project_path(name)).read() for name in (
        'README.rst',
        'HACKING.rst',
        'CHANGES.rst',
    )),

    namespace_packages=['gocept'],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    data_files=[('',
                 glob.glob(project_path('*.rst')),
                 glob.glob(project_path('*.rst')))],
    zip_safe=False,
)
