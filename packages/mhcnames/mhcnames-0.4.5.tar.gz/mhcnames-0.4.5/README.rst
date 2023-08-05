mhcnames
========

All the fun and adventure of MHC nomenclature, now in Python

Example
-------

.. code:: python

    In [1]: mhcnames.parse_allele_name("HLA-A0201")
    Out[1]: AlleleName(species='HLA', gene='A', allele_family='02', allele_code='01')

    In [2]: mhcnames.compact_allele_name("HLA-A*02:01")
    Out[2]: 'A0201'
