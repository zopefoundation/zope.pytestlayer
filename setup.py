"""Integration of zope.testrunner-style test layers into pytest framework"""

from setuptools import setup


setup(
    name='zope.pytestlayer',
    version='9.0',

    python_requires='>=3.9',
    install_requires=[
        'pytest >= 8',
        'setuptools',
        'zope.dottedname',
    ],

    extras_require={
        'test': [
            'plone.testing',
        ],
        'docs': [
            'Sphinx',
            'gocept.package',
        ]
    },

    entry_points={
        'pytest11': [
            'zopelayer = zope.pytestlayer.plugin',
        ],
    },

    author='gocept',
    author_email='zope-dev@zope.dev',
    license='ZPL-2.1',
    url='https://github.com/zopefoundation/zope.pytestlayer/',

    keywords='pytest zope.testrunner layer fixture',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Framework :: Pytest",
        "Framework :: Plone",
        "Framework :: Zope :: 3",
        "Framework :: Zope :: 5",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Zope Public License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
    ],
    description=__doc__.strip(),
    long_description='\n\n'.join(open(name).read() for name in (
        'README.rst',
        'HACKING.rst',
        'CHANGES.rst',
    )),
    include_package_data=True,
    zip_safe=False,
)
