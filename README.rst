.. raw:: html

   <p align="center">
        <a href='https://npyfile.readthedocs.io/en/latest/?badge=latest'>
            <img src='https://readthedocs.org/projects/npyfile/badge/?version=latest' alt='Documentation Status' />
        </a>
        <a href="https://github.com/maxstrobel/npyfile/actions?workflow=CI">
          <img src="https://github.com/maxstrobel/npyfile/workflows/CI/badge.svg?branch=master" alt="CI Status" />
        </a>
        <a href="https://codecov.io/gh/maxstrobel/npyfile">
          <img src="https://codecov.io/gh/maxstrobel/npyfile/branch/master/graph/badge.svg?token=W2IITSWUH4"/>
        </a>
   </p>

.. teaser-begin

``npyfile``: Write arrays continuously to ``.npy`` files
========================================================

``npyfile`` is a a package that allows you to continuously write arrays to a ``.npy`` file. You can use it like a
standard Python file with the well-known context manager.

*Warning*: Due to the internal structure of ``.npy`` files, the arrays must have the same ``shape`` & ``dtype``.

.. teaser-end

Example
-------
Generate some artificial dummy data, e.g. images, & write them into a temporary file. A real world scenario reflecting
this is the continuous arrival of new images from a camera.

.. code-block:: python

    import pathlib
    import tempfile
    tmp_dir = tempfile.TemporaryDirectory()
    outfile = pathlib.Path(tmp_dir.name) / 'images.npy'

    images = np.random.randint(low=0, high=255, size=(10,640,480,3))

    with NpyFile(outfile) as file:
        for img in images:
            file.write(img)

    np.testing.assert_array_equal(images, np.load(outfile))

    tmp_dir.cleanup()



Credits
-------

- `attrs`_: Project & infrastructure setup
- `numpy`_: File format


.. _attrs:
    https://www.attrs.org
.. _numpy:
    https://numpy.org/