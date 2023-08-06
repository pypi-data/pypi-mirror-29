meshio
======

|CircleCI| |codecov| |Codacy grade| |PyPi Version| |DOI| |GitHub stars|

.. figure:: https://nschloe.github.io/meshio/meshio_logo.png
   :alt: 
   :width: 20.0%

There are various mesh formats available for representing unstructured
meshes, e.g.,

-  `ANSYS
   msh <http://www.afs.enea.it/fluent/Public/Fluent-Doc/PDF/chp03.pdf>`__
-  `DOLFIN
   XML <http://manpages.ubuntu.com/manpages/wily/man1/dolfin-convert.1.html>`__
-  `Exodus <https://cubit.sandia.gov/public/13.2/help_manual/WebHelp/finite_element_model/exodus/block_specification.htm>`__
-  `H5M <https://www.mcs.anl.gov/~fathom/moab-docs/h5mmain.html>`__
-  `Medit <https://people.sc.fsu.edu/~jburkardt/data/medit/medit.html>`__
-  `MED/Salome <http://docs.salome-platform.org/latest/dev/MEDCoupling/med-file.html>`__
-  `Gmsh <http://gmsh.info/doc/texinfo/gmsh.html#File-formats>`__
-  `OFF <http://segeval.cs.princeton.edu/public/off_format.html>`__
-  `PERMAS <http://www.intes.de>`__
-  `STL <https://en.wikipedia.org/wiki/STL_(file_format)>`__
-  `VTK <https://www.vtk.org/wp-content/uploads/2015/04/file-formats.pdf>`__
-  `VTU <https://www.vtk.org/Wiki/VTK_XML_Formats>`__
-  `XDMF <http://www.xdmf.org/index.php/XDMF_Model_and_Format>`__

meshio can read and write all of these formats and smoothly converts
between them. Simply call

::

    meshio-convert input.msh output.vtu

with any of the supported formats.

In Python, simply call

.. code:: python

    points, cells, point_data, cell_data, field_data = \
        meshio.read(args.infile)

to read a mesh. To write, do

.. code:: python

    points = numpy.array([
        [0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        ])
    cells = {
        'triangle': numpy.array([
            [0, 1, 2]
            ])
        }
    meshio.write(
        'foo.vtk',
        points,
        cells,
        # Optionally provide extra data on points, cells, etc.
        # point_data=point_data,
        # cell_data=cell_data,
        # field_data=field_data
        )

For both input and output, you can optionally specify the exact
``file_format`` (in case you would like to enforce binary over ASCII
VTK, for example).

Installation
~~~~~~~~~~~~

meshio is `available from the Python Package
Index <https://pypi.python.org/pypi/meshio/>`__, so simply type

::

    pip install -U meshio

to install or upgrade.

Usage
~~~~~

Just

::

    import meshio

and make use of all the goodies the module provides.

Testing
~~~~~~~

To run the meshio unit tests, check out this repository and type

::

    pytest

Distribution
~~~~~~~~~~~~

To create a new release

1. bump the ``__version__`` number,

2. tag and upload to PyPi:

   ::

       make publish

License
~~~~~~~

meshio is published under the `MIT
license <https://en.wikipedia.org/wiki/MIT_License>`__.

.. |CircleCI| image:: https://img.shields.io/circleci/project/github/nschloe/meshio/master.svg
   :target: https://circleci.com/gh/nschloe/meshio
.. |codecov| image:: https://img.shields.io/codecov/c/github/nschloe/meshio.svg
   :target: https://codecov.io/gh/nschloe/meshio
.. |Codacy grade| image:: https://img.shields.io/codacy/grade/dc23fe7f7d4540b0a405110b3ae97dc6.svg
   :target: https://app.codacy.com/app/nschloe/meshio/dashboard
.. |PyPi Version| image:: https://img.shields.io/pypi/v/meshio.svg
   :target: https://pypi.python.org/pypi/meshio
.. |DOI| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.1173115.svg
   :target: https://doi.org/10.5281/zenodo.1173115
.. |GitHub stars| image:: https://img.shields.io/github/stars/nschloe/meshio.svg?logo=github&style=social&label=Stars
   :target: https://github.com/nschloe/meshio


