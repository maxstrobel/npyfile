import pytest
from npyfile import NpyFile
import numpy as np


@pytest.fixture
def tmp_file(tmp_path):
    tmp_file = tmp_path / 'test.npy'
    return tmp_file


def test_no_write(tmp_file):
    with NpyFile(tmp_file):
        pass
    assert tmp_file.stat().st_size == 0, "File should be empty."


def test_auto_suffix(tmp_path):
    tmp_file = tmp_path / 'test'
    with NpyFile(tmp_file):
        pass
    assert tmp_file.with_suffix('.npy').exists(), 'Suffix should be .npy.'


@pytest.mark.parametrize('n_iterations', range(1, 10))
def test_multiple_writes(n_iterations, tmp_file):
    data = np.arange(n_iterations)[:, None]
    with NpyFile(tmp_file) as f:
        for x in data:
            f.write(x)

    np.testing.assert_array_equal(np.load(tmp_file), data)


@pytest.mark.parametrize('dtype', [
    'int8', 'int16', 'int32', 'int64', 'uint8', 'uint16', 'uint32', 'uint64',
    'float16', 'float32', 'float64', 'complex64', 'complex128',
])
@pytest.mark.parametrize('fortran', [True, False])
@pytest.mark.parametrize('shape', [(2,) * i for i in range(1, 8)])
def test_different_arrays(dtype, fortran, shape, tmp_file):
    N_ITERATIONS = 5
    n_elements = N_ITERATIONS * np.prod(shape)
    data = np.random.randn(n_elements)

    data = data.astype(dtype)
    if fortran:
        data = np.asfortranarray(data)
    data = data.reshape((N_ITERATIONS,) + shape)

    with NpyFile(tmp_file) as f:
        for x in data:
            f.write(x)

    data_ = np.load(tmp_file)
    assert data.dtype == data_.dtype
    assert data.data.c_contiguous == data_.data.c_contiguous
    assert data.data.f_contiguous == data_.data.f_contiguous
    assert data.shape == data_.shape
    np.testing.assert_array_equal(data, data_)


@pytest.mark.parametrize('x,y', [
    (np.zeros((2, 2)), np.ones((3, 2))),
    (np.zeros((2, 2), dtype='uint8'), np.ones((2, 2), dtype='float16')),
    (np.zeros((2, 2)), np.asfortranarray(np.ones((2, 2)))),
], ids=[
    'Different shape',
    'Different dtype',
    'Different memory layout',
])
def test_assertions(x, y, tmp_file):
    with NpyFile(tmp_file) as f:
        f.write(x)

        with pytest.raises(AssertionError):
            f.write(y)
