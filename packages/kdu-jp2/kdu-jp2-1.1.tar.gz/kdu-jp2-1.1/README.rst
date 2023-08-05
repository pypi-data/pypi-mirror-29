Python library for batch conversion to JP2 using kdu_compress
==========================


Installation and Use
--------------------
#. Install the package: ``pip install kdu-jp2``
#. Import the library: ``from kdu_jp2 import JP2Converter``
#. Create an instance: ``converter = JP2Converter('in_dir', 'out_dir')``
#. Run the conversion: ``converter.convert()`` (lossy) or ``converter.convert(True)`` (lossless)


System requirements
-------------------

This depends on Kakadu - ``kdu_compress`` must be on your path.

.. _progressbar33: http://pythonhosted.org/progressbar33/
