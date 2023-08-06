access2theMatrix is a Python library for accessing Scienta Omicron
(NanoScience) (NanoTechnology) MATRIX Control System result files.
Scanning Probe Microscopy (SPM) Image data, Single Point Spectroscopy
(SPS) Curve data and Phase/Amplitude Curve data will be accessed by
this library. access2theMatrix is pure Python.

The library access2theMatrix has the package access2thematrix which in turn
contains the module access2thematrix. The class MtrxData in the access2thematrix
module has the methods to open SPM Image, SPS Curve and Phase/Amplitude Curve
result files, to select one out of the four possible traces (forward/up,
backward/up, forward/down and backward/down) for images and to select one out of
the two possible traces (trace, retrace) for curves. Includes method for
experiment element parameters overview.

Dependencies
------------
access2theMatrix requires the NumPy (http://www.numpy.org) and the six
(https://pypi.python.org/pypi/six/) library.

Installation
------------
Using pip::

    > pip install access2theMatrix

Example usage
-------------
In this example the MATRIX Control System has stored the acquired data in the
folder ``c:\data``. In addition to the result data files the folder must also
contain the result file chain, see the MATRIX Application Manual for SPM.
The image file ``Au(111) bbik fe-20151110-112314--3_1.Z_mtrx`` will be opened
and the ``forward/up`` trace will be selected.

.. code-block:: pycon

    >>> import access2thematrix
    >>> mtrx_data = access2thematrix.MtrxData()
    >>> data_file = r'c:\data\Au(111) bbik fe-20151110-112314--3_1.Z_mtrx'
    >>> traces, message = mtrx_data.open(data_file)
    >>> traces
    {0: 'forward/up', 1: 'backward/up'}
    >>> im, message = mtrx_data.select_image(traces[0])
    >>>

The variable ``im`` will contain the data and the metadata of the selected
image and the ``im`` object has the initial attributes ``data``, ``width``,
``height``, ``y_offset``, ``x_offset``, ``angle`` and ``channel_name_and_unit``.
We will continue the example by opening de curve file
``Au(111) bbik fe-20151110-112314--2_1.Aux2(V)_mtrx`` and selecting the
``retrace`` trace.

.. code-block:: pycon

    >>> data_file = r'c:\data\Au(111) bbik fe-20151110-112314--2_1.Aux2(V)_mtrx'
    >>> traces, message = mtrx_data.open(data_file)
    >>> traces
    {0: 'trace', 1: 'retrace'}
    >>> cu, message = mtrx_data.select_curve(traces[1])
    >>>

The variable ``cu`` will contain the data and the metadata of the selected
curve and the ``cu`` object has the initial attributes ``data``,
``referenced_by``, ``x_data_name_and_unit`` and ``y_data_name_and_unit``.

To get a list and a printable sorted text list of the experiment element
parameters with their values and units, use the method
``get_experiment_element_parameters``.

Authors & affiliations
----------------------
Stephan J. M. Zevenhuizen [#]_

..  [#] Condensed Matter and Interfaces, Debye Institute for Nanomaterials
    Science, Utrecht University, Utrecht, The Netherlands.


