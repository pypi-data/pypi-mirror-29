Mummichog
=========

Mummichog is a Python program for analyzing data from high throughput, untargeted metabolomics. It leverages the organization of metabolic networks to predict functional activity directly from feature tables, bypassing metabolite identification. The features include

* computing significantly enriched metabolic pathways
* identifying significant modules in the metabolic network
* visualization of top networks in web browser
* visualization that also plugs into Cytoscape
* tentative annotations
* metabolic models for different species through plugins

Version 2 adds retention time for grouping ions, and improves adduct calculation and data tracking. The overall design has changed considerably to make the software more modular, easier to integrate into web services.
There is a separate version 1 package on PyPi as 'mummichog1'.
This package is provided for the convenience of developers and users, while the development of mummichog is swtiching more to web-based services.


Installation
------------
Mummichog can be installed using pip (pip Installs Packages), the Python package manager:

::

    pip install mummichog

This is OS independent. To read more on pip `here <https://pip.pypa.io/en/stable/installing/#installing-with-get-pip-py>`.

One can also run mummichog without installing it. Direct python call on a downloaded copy will work.
Note: a common error may come up in earlier versions as

::

    AttributeError: 'NoveView' object has no attribute 'sort'

This is caused by an incompatible update in networkx-2.0 library. It can be fixed by specifying

::

    sudo pip install networkx==1.10

Usage
-----
Input data are a tab-delimited file with the first 4 columns in this order:

::

	mz      rtime   p-value t-score
	186.0185697     463     0.000149751400132       3.82
	279.1773473     90      0.000399613326314       3.56
	344.1330624     124     0.000998323061251       -3.31
	215.9641894     132     0.00105418285794        -3.29
	177.0323244     77     0.00121065359218        3.25

The command line to run mummichog is like this:

::

	mummichog -f testdata0710.txt -o myoutput


The initial paper on mummichog is described in Li et al. Predicting Network Activity from High Throughput Metabolomics. PLoS Computational Biology (2013); doi:10.1371/journal.pcbi.1003123.. More on `project website <http://mummichog.org>`.
