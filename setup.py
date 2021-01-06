import re
from pathlib import Path

from setuptools import setup, find_packages

###############################################################################

# Package meta-data.
NAME = 'npyfile'
PROJECT_URLS = {
    'Documentation': 'https://npyfile.readthedocs.io/',
    'Source Code': 'https://github.com/maxstrobel/npyfile',
    'Bug Tracker': 'https://github.com/maxstrobel/npyfile/issues',
}
CLASSIFIERS = [
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: Implementation :: CPython',
    'Topic :: Scientific/Engineering',
    'Topic :: Software Development',
    'Typing :: Typed',
]
PYTHON_REQUIRES = '>=3.6'

# What packages are required for this module to be executed?
INSTALL_REQUIRES = ['numpy']

# What packages are optional?
EXTRAS_REQUIRE = {
    'docs': ['sphinx', 'sphinx_autodoc_typehints', 'sphinx-rtd-theme'],
    'tests': ['coverage', 'pytest', 'tox'],
}
EXTRAS_REQUIRE['dev'] = (EXTRAS_REQUIRE['docs'] + EXTRAS_REQUIRE['tests'])

# Define here entry points for the package
ENTRY_POINTS = {
    'console_scripts': []
}


###############################################################################


def read(rel_path):
    HERE = Path(__file__).resolve().parent
    with open(HERE / rel_path, 'r', encoding='utf-8') as f:
        return f.read()


# Meta data is stored on package level __init__.py -> Meta data also accessible in python
META_FILE = read(f'src/{NAME}/__init__.py')


def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(f"""^__{meta}__ = ['"]([^'"]*)['"]""", META_FILE, re.M)
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError(f'Unable to find __{meta}__ string.')


# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
DESCRIPTION = find_meta('description')
try:
    LONG = read('README.rst').split(".. teaser-begin")[1]
except FileNotFoundError:
    LONG = DESCRIPTION

# Where the magic happens:
setup(
    name=NAME,
    version=find_meta('version'),
    description=DESCRIPTION,
    long_description=LONG,
    long_description_content_type='text/x-rst',
    author=find_meta('author'),
    author_email=find_meta('email'),
    maintainer=find_meta('author'),
    maintainer_email=find_meta('email'),
    python_requires=PYTHON_REQUIRES,
    url=find_meta('url'),
    project_urls=PROJECT_URLS,
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    entry_points=ENTRY_POINTS,
    classifiers=CLASSIFIERS,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    include_package_data=True,
)
