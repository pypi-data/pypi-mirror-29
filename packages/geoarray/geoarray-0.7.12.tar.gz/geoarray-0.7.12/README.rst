========
geoarray
========


Fast Python interface for geodata - either on disk or in memory.


* Free software: GNU General Public License v3
* Documentation: http://danschef.gitext.gfz-potsdam.de/geoarray/doc/


Status
------

.. .. image:: https://img.shields.io/travis/danschef/geoarray.svg
        :target: https://travis-ci.org/danschef/geoarray

.. .. image:: https://readthedocs.org/projects/geoarray/badge/?version=latest
        :target: https://geoarray.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. .. image:: https://pyup.io/repos/github/danschef/geoarray/shield.svg
     :target: https://pyup.io/repos/github/danschef/geoarray/
     :alt: Updates

.. image:: https://gitext.gfz-potsdam.de/danschef/geoarray/badges/master/build.svg
        :target: https://gitext.gfz-potsdam.de/danschef/geoarray/commits/master
.. image:: https://gitext.gfz-potsdam.de/danschef/geoarray/badges/master/coverage.svg
        :target: http://danschef.gitext.gfz-potsdam.de/geoarray/coverage/
.. image:: https://img.shields.io/pypi/v/geoarray.svg
        :target: https://pypi.python.org/pypi/geoarray
.. image:: https://img.shields.io/pypi/l/geoarray.svg
        :target: https://gitext.gfz-potsdam.de/danschef/geoarray/blob/master/LICENSE
.. image:: https://img.shields.io/pypi/pyversions/geoarray.svg
        :target: https://img.shields.io/pypi/pyversions/geoarray.svg


See also the latest coverage_ report and the nosetests_ HTML report.


Features
--------

* TODO


Installation
------------
geoarray depends on some open source packages which are usually installed without problems by the automatic install
routine. However, for some projects, we strongly recommend resolving the dependency before the automatic installer
is run. This approach avoids problems with conflicting versions of the same software.
Using conda_, the recommended approach is:

 .. code-block:: console

    # create virtual environment for geoarray, this is optional
    conda create -y -q --name geoarray python=3
    source activate geoarray
    conda install -y -q -c conda-forge numpy gdal scikit-image matplotlib pandas rasterio pyproj basemap shapely geopandas
    conda install --yes -c ioam bokeh holoviews  # optional


To install geoarray, use the pip installer:

.. code-block:: console

    pip install geoarray


* Or clone the repository via GIT and update the PATH environment variable:

.. code-block:: console

    cd /your/installation/folder
    git clone https://gitext.gfz-potsdam.de/danschef/geoarray.git
    PATH=$PATH:~/path/to/your/installation/folder/geoarray


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _coverage: http://danschef.gitext.gfz-potsdam.de/geoarray/coverage/
.. _nosetests: http://danschef.gitext.gfz-potsdam.de/geoarray/nosetests_reports/nosetests.html
.. _conda: https://conda.io/docs/
