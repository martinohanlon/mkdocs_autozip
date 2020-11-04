import sys
from setuptools import setup

if sys.version_info[0] == 2:
    raise ValueError('This package requires Python 3.5 or newer')
elif sys.version_info[0] == 3:
    if not sys.version_info >= (3, 5):
        raise ValueError('This package requires Python 3.5 or newer')
else:
    raise ValueError('Unrecognized major version of Python')

__project__ = "mkdocs_autozip"
__package__ = "mkdocs_autozip"
__version__ = '0.2.0'
__author__ = "Martin O'Hanlon"
__desc__ = 'A mkdocs plugin for zipping source files during build.'
__author_email__ = 'martin.ohanlon@raspberrypi.org'
__url__ = 'https://github.com/martinohanlon/mkdocs_autozip'
__requires__ = ["mkdocs", "requests"]
__keywords__ = [
    "mkdocs",
    "zip",
    "plugin",
]

__classifiers__ = [
   "Development Status :: 4 - Beta",
#    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Topic :: Education",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
]
__long_description__ = """# mkdocs autozip

A mkdocs plugin for zipping source files during build.
"""

if __name__ == '__main__':
    setup(
        name=__project__,
        version = __version__,
        description = __desc__,
        long_description=__long_description__,
        long_description_content_type='text/markdown',
        url = __url__,
        author = __author__,
        author_email = __author_email__,
        classifiers=__classifiers__,
        keywords=__keywords__,
        packages = [__package__],
        install_requires = __requires__,
        entry_points={
        'mkdocs.plugins': [
            'autozip = mkdocs_autozip:AutoZipPlugin',
            ]
        },
        zip_safe=False)