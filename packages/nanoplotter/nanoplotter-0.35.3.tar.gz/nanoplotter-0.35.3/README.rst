nanoplotter
===========

This module provides functions for plotting data extracted from Oxford
Nanopore sequencing reads and alignments, but some of it's functions can
also be used for other applications.

|Twitter URL| |install with conda| |Build Status| |Code Health|

FUNCTIONS
---------

-  Check if a specified color is a valid matplotlib color
   ``checkvalidColor(color)``
-  Check if a specified output format is valid
   ``checkvalidFormat(format)``
-  Create a bivariate plot with dots, hexbins and/or kernel density
   estimates. Also arguments for specifying axis names, color and
   xlim/ylim.
   ``scatter(x, y, names, path, color, format, plots, stat=None, log=False, minvalx=0, minvaly=0)``
-  Create cumulative yield plot and evaluate read length and quality
   over time ``timePlots(df, path, color, format)``
-  Create length distribution histogram and density curve
   ``lengthPlots(array, name, path, n50, color, format, log=False)``
-  Create flowcell physical layout in numpy array ``makeLayout()``
-  Present the activity (number of reads) per channel on the flowcell as
   a heatmap ``spatialHeatmap(array, title, path, color, format)``

INSTALLATION
------------

.. code:: bash

    pip install nanoplotter

| or
| |install with conda|

::

    conda install -c bioconda nanoplotter

STATUS
------

|Build Status| |Code Health|

.. |Twitter URL| image:: https://img.shields.io/twitter/url/https/twitter.com/wouter_decoster.svg?style=social&label=Follow%20%40wouter_decoster
   :target: https://twitter.com/wouter_decoster
.. |install with conda| image:: https://anaconda.org/bioconda/nanoplotter/badges/installer/conda.svg
   :target: https://anaconda.org/bioconda/nanoplotter
.. |Build Status| image:: https://travis-ci.org/wdecoster/nanoplotter.svg?branch=master
   :target: https://travis-ci.org/wdecoster/nanoplotter
.. |Code Health| image:: https://landscape.io/github/wdecoster/nanoplotter/master/landscape.svg?style=flat
   :target: https://landscape.io/github/wdecoster/nanoplotter/master
