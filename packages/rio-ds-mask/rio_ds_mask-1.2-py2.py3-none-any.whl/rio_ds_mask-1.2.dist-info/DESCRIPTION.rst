===========
rio-ds-mask
===========

A `Rasterio <https://github.com/mapbox/rasterio>`__ plugin for extracting
an image's dataset-level mask.

.. image:: https://travis-ci.org/geowurster/rio-ds-mask.svg?branch=master
    :target: https://travis-ci.org/geowurster/rio-ds-mask

.. image:: https://coveralls.io/repos/github/geowurster/rio-ds-mask/badge.svg?branch=master
    :target: https://coveralls.io/github/geowurster/rio-ds-mask


=====
Usage
=====

.. code-block:: console

    Usage: rio ds-mask [OPTIONS] INPUT OUTPUT

      Extract an image's dataset-level mask.

      Both output driver and datatype are derived from the input image if not
      given.

      In some cases this plugin alters GDAL's returned mask values.  When
      writing masks GDAL uses 0's for opaque and 255's for transparent, but when
      reading masks the returned value differs based on the image's datatype.  8
      bit images produce 8 bit masks where 0's are opaque and 255's are
      transparent, however 16 bit images use 0's for opaque and 1's for
      transparent, still stored as 8 bit.  If the image's datatype is 'int16' or
      'uint16' and the mask's maximum value is 1, then all 1's are translated to
      255's.  The mask's datatype is preserved.  I have not fully investigated
      all of GDAL's masking options to determine if the behavior is consistent.
      If it is found to be a deliberate choice then the normalization will be
      removed.

    Options:
      -f, --format, --driver TEXT     Output format driver
      -t, --dtype [ubyte|uint8|uint16|int16|uint32|int32|float32|float64]
                                      Output data type.
      --co, --profile NAME=VALUE      Driver specific creation options.See the
                                      documentation for the selected output driver
                                      for more information.
      --help                          Show this message and exit.

This example command creates a singleband ``uint8`` image that is acceptable
to use as a GDAL mask band, meaning that pixels with a value of ``255`` are
transparent and pixels with a vaue of ``0`` are opaque.  The image is
losslessly compressed and internally tiled.

.. code-block:: console

    $ rio ds-mask \
        --driver GTiff \
        tests/data/alpha.tif \
        mask.tif \
        --co COMPRESS=DEFLATE \
        --co TILED=YES


==========
Installing
==========

First `install Rasterio <http://mapbox.github.io/rasterio/installation.html>`__,
then:

.. code-block:: console

    $ pip install rio-ds-mask --user


Developing
==========

.. code-block:: console

    $ git clone https://github.com/geowurster/rio-ds-mask.git
    $ cd rio-ds-mask
    $ pip install -e .\[all\]
    $ pytest --cov rio-ds-mask --cov-report term-missing


License
=======

See `LICENSE.txt <LICENSE.txt>`__


Changelog
=========

See `CHANGES.md <CHANGES.md>`__

