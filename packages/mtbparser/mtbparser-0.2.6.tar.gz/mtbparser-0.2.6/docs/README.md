# Documentation

## File Formats

In total, this module provides parsers for **four** different information formats, that have been specified for data provisioning to the Molecular Tumor Board.

Formats for:

* [Somatic SNVs](./somatic_snvs.md)
* [Somatic CNVs](./cnvs.md)
* [Somatic structural variants](./structural_variants.md)
* [Germline SNVs](./germline_snvs.md)
* [Germline CNVs](./cnvs.md)
* [Metadata](./metadata.md)

All file formats are **tab separated** (tsv).

## Parser Classes

With respect to the format definitions, these parsers are available in ``mtbparser``:

* SNVParser

### How to use the SnvParser class

Parsing a SNV file following the formats described above is fairly simple. Just create an ``SnvParser`` object with the path to the ``tsv``-file and specify its type by providing the correct header (``SSnvHeader, GSnvHeader, ...``).

```python
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

```