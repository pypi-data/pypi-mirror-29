nanoQC
======

Quality control tools for long read sequencing data aiming to replicate
some of the plots made by fastQC.

|Twitter URL| |install with conda|

Creates dynamic plots using
`bokeh <https://bokeh.pydata.org/en/latest/>`__. For an example see
`here <http://decoster.xyz/wouter/>`__

INSTALLATION
------------

.. code:: bash

    pip install nanoQC

| or
| |install with conda|

::

    conda install -c bioconda nanoqc

USAGE
-----

::

    nanoQC [-h] [-v] [-o OUTDIR] fastq

    positional arguments:
      fastq                 Reads data in fastq.gz format.

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         Print version and exit.
      -o, --outdir OUTDIR   Specify directory in which output has to be created.

.. |Twitter URL| image:: https://img.shields.io/twitter/url/https/twitter.com/wouter_decoster.svg?style=social&label=Follow%20%40wouter_decoster
   :target: https://twitter.com/wouter_decoster
.. |install with conda| image:: https://anaconda.org/bioconda/nanoqc/badges/installer/conda.svg
   :target: https://anaconda.org/bioconda/nanoqc
