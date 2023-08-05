=====
PyUNC
=====

PyUNC is a Python module for reading the UNC MRI image format it is also able
to convert UNC format images to NIFTI format.


Example
-------

.. code:: python

    from pyunc import UNCFile

    unc = UNCFile.from_path('filename.unc')

    # get the image title
    unc.title

    # get the image data as a numpy matrix
    unc.pixels


Installation
------------

.. code:: shell

    git clone https://github.com/jstutters/pyunc
    cd pyunc
    pip install .


Requirements
------------

pyunc is tested with Python v2.7 and 3.4.  The module will install numpy and
nibabel as dependencies.


Contribute
----------

- Issue Tracker: `github.com/jstutters/pyunc/issues <http://github.com/jstutters/pyunc/issues>`_
- Source Code: `github.com/jstutters/pyunc <http://github.com/jstutters/pyunc>`_


Support
-------

If you are having problems, please let me know by submitting an issue in the tracker.


