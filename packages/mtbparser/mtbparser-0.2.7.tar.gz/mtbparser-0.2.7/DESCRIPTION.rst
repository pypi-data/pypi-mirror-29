About this module
=================
This Python module was designed to provide a simple parser for different diagnostic variant information data.

How to use the SnvParser class
==============================

Parsing a SNV file following the formats described above is fairly simple. Just create an ``SnvParser`` object with the path to the ``tsv``-file and specify its type by providing the correct header (``SSnvHeader, GSnvHeader, ...``).

.. code-block:: python
    
    from mtbparser.snv_parser import SnvParser
    from mtbparser.snv_utils import SSnvHeader

    # Path to a valid SNV tsv file, as specified in
    # the file format documentation.
    somatic_snv_file = "/path/to/mySSnv.tsv"

    # Create parser object for somatic SNVs
    parser = SnvParser(somatic_snv_file, SSnvHeader)

    # Iterate through parsed SNV items and get the gene name
    for snv_item in parser.getSNVs():
        print(snv_item.get_snv_info(SSnvHeader.GENE.name))

        
Detailed documentation
======================

A more detailed documentation can be found on `Github <https://github.com/qbicsoftware/qbic.mtbparser>`_.
    
