"""Package for writing continuously NpyFiles.

This package contains an implementation to write continuously to a ``.npy``
file. It is useful if single slices of an array are available sequentially,
i.e. from a live camera that delivers images over time, or do not fit into the
memory.

The `Numpy file format`_ is a simple binary format with a header followed by the
actual data.

.. _Numpy file format:
    https://numpy.org/doc/stable/reference/generated/numpy.lib.format.html
"""

from npyfile.npyfile import NpyFile

__version__ = '1.0.0'
__description__ = 'NumPy File'
__url__ = 'https://github.com/maxstrobel/npyfile'
__author__ = 'Maximilian Strobel'
__email__ = 'max.strobel28@gmail.com'
__license__ = 'MIT'
__copyright__ = 'Copyright (C) 2021 Maximilian Strobel'
