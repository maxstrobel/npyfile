"""Implementation of the NpyFile."""
import struct
from pathlib import Path
from types import TracebackType
from typing import Union, Optional, Type, Tuple, TypeVar

import numpy as np

MAJOR_VERSION = 1
MINOR_VERSION = 0
HEADER_LENGTH = 2038

_NpyFile = TypeVar('_NpyFile', bound='NpyFile')


class NpyFile:
    """NpyFile

    A file-like object to continuously write data slices into a ``.npy`` NumPy
    file.

    Warnings:
        The ``shape``, ``dtype`` & memory view should not change for a file.

    Examples:
        TemporaryDirectory for demonstration purpose. You should use a real file:

        >>> import pathlib
        >>> import tempfile
        >>> tmp_dir = tempfile.TemporaryDirectory()
        >>> outfile = pathlib.Path(tmp_dir.name) / 'images.npy'

        Generate stack of 10 random images (could also arrive from a live cam):

        >>> images = np.random.randint(low=0, high=255, size=(10,640,480,3))

        Write the data image by image to the file:

        >>> with NpyFile(outfile) as file:
        ...     for img in images:
        ...         file.write(img)

        Show equivalence between the original & stored data.

        >>> np.testing.assert_array_equal(images, np.load(outfile))

        Clean-up TemporaryDirectory.

        >>> tmp_dir.cleanup()

    References:
        - `Numpy file format`_

    .. _Numpy file format:
        https://numpy.org/doc/stable/reference/generated/numpy.lib.format.html
    """

    def __init__(self, filename: Union[str, Path]):
        """Initialize a NpyFile object.

        It is used to save continuous slices of an array to a binary file in
        NumPy ``.npy`` format.

        Args:
            filename: Filename to which the data is saved. A ``.npy`` extension
            will be appended to the filename if it does not already have one.
        """
        filename = Path(filename)
        if not filename.name.endswith('.npy'):
            filename = filename.parent / (filename.name + '.npy')
        self._file = filename.open('wb')
        self._file.seek(HEADER_LENGTH + 10)

        self._dtype: Optional[np.dtype] = None
        self._fortran_order: Optional[bool] = None
        self._shape: Optional[Tuple[int, ...]] = None

        self._frame_number: int = 0

    def __enter__(self: _NpyFile) -> _NpyFile:
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]],
                 exc_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> None:
        self.close()

    def write(self, data: np.ndarray) -> None:
        """Write a data slice into the file.

        Args:
            data: Slice to write.
        """
        if self._dtype is None:
            self._dtype = data.dtype
        if self._fortran_order is None:
            self._fortran_order = (
                    data.flags.f_contiguous and not data.flags.c_contiguous
            )
        if self._shape is None:
            self._shape = data.shape

        assert self._dtype == data.dtype, 'Type must not change.'
        assert self._fortran_order == (
                data.flags.f_contiguous and not data.flags.c_contiguous
        ), 'Memory layout must not change.'
        assert self._shape == data.shape, 'Shape must not change.'

        data = np.asanyarray(data)
        data = data.tobytes('C' if not self._fortran_order else 'F')
        self._file.write(data)
        self._frame_number += 1

    def close(self) -> None:
        """Close the file."""
        if self._frame_number > 0:
            self._write_header()
        self._file.close()

    def _write_header(self) -> None:
        """Write the header of a .npy file to the start of the file."""
        assert self._dtype is not None, 'Type must be known.'
        assert self._fortran_order is not None, 'Memory layout must be known.'
        assert self._shape is not None, 'Shape must be known.'

        self._shape = (self._frame_number,) + self._shape

        magic = np.lib.format.magic(MAJOR_VERSION, MINOR_VERSION)
        length = struct.pack("<H", HEADER_LENGTH)
        array_format = (
            f"{{'descr' : '{np.lib.format.dtype_to_descr(self._dtype)}', "
            f"'fortran_order': {self._fortran_order}, "
            f"'shape': ({', '.join([str(x) for x in self._shape])}), }}"
        ).ljust(HEADER_LENGTH)

        header = bytes(magic) + length + bytes(array_format, encoding='ascii')

        self._file.seek(0)
        self._file.write(header)
