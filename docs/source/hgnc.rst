.. _HGNC:

HGNC
====

We want to pay tribute to the `HGNC database of human gene names <http://www.genenames.org/>`_
and HUGO Gene Nomenclature Committee team for their
amazing resource their provide to the scientific community.
:code:`pyhgnc` only provides methods to download and locally query open accessible
HGNC data available on `EBI ftp server <ftp://ftp.ebi.ac.uk/pub/databases/genenames/>`_.

About
-----

Citation from `EBI HGNC website <https://www.ebi.ac.uk/services/teams/hgnc>`_ [23/11/2017]:
    "HGNC is the only worldwide authority assigning standardised human gene symbols and names. Its key goals are
    to provide unique standardised nomenclature for every human gene; to ensure this information is freely available,
    widely disseminated and universally used; and to coordinate the expansion and utilisation of this nomenclature
    across vertebrates."

Citation
--------

*Latest HGNC publication:*

`Gray KA, Yates B, Seal RL, Wright MW, Bruford EA. genenames.org: the HGNC resources in 2015. Nucleic Acids Res.
2015 Jan;43(Database issue):D1079-85. doi: 10.1093/nar/gku1071.
PMID:25361968 <https://www.ncbi.nlm.nih.gov/pubmed/25361968>`_


HGNC Database, HUGO Gene Nomenclature Committee (HGNC), EMBL Outstation - Hinxton, European Bioinformatics Institute,
Wellcome Trust Genome Campus, Hinxton, Cambridgeshire, CB10 1SD, UK www.genenames.org.

Links
-----

*Link to data:* `EBI ftp server <ftp://ftp.ebi.ac.uk/pub/databases/genenames/>`_

Check the `HGNC database of human gene names <http://www.genenames.org/>`_ for more information.

HCOP
====

PyHGNC integrates also HGNC Comparison of Orthology Predictions (HCOP).

About
-----

HCOP is a tool that integrates
orthology assertions predicted for a specified human gene, or set of human genes, by

- `eggNOG <http://eggnog.embl.de>`_
- `Ensembl Compara <http://www.ensembl.org/info/genome/compara>`_
- `HGNC <http://www.genenames.org/>`_
- `HomoloGene <https://www.ncbi.nlm.nih.gov/homologene>`_
- `Inparanoid <http://inparanoid.sbc.su.se>`_
- `NCBI Gene Orthology <https://www.ncbi.nlm.nih.gov/books/NBK3841/#EntrezGene.General_Gene_Information>`_
- `OMA <http://omabrowser.org>`_
- `OrthoDB <http://www.orthodb.org/>`_
- `OrthoMCL <http://orthomcl.org/orthomcl/>`_
- `Panther <http://www.pantherdb.org/>`_
- `PhylomeDB <http://phylomedb.org/>`_
- `TreeFam <http://www.treefam.org/>`_
- `ZFIN <http://zfin.org/>`_

 An indication of the reliability of a prediction is provided by the number of databases which concur.
 HCOP was originally designed to show orthology predictions between human and mouse, but has been expanded to
 include data from chimp, macaque, rat, dog, horse, cow, pig, opossum, platypus, chicken, anole lizard, xenopus,
 zebrafish, C. elegans, Drosophila and S. cerevisiae, meaning that there are currently 18 genomes available
 for comparison in HCOP.

Citation
--------

- Wright MW, Eyre TA, Lush MJ, Povey S and Bruford EA.
    HCOP: The HGNC Comparison of Orthology Predictions Search Tool.
    Mamm Genome. 2005 Nov; 16(11):827-828. PMID:`16284797 <https://www.ncbi.nlm.nih.gov/pubmed/16284797>`_
    `PDF <http://www.genenames.org/sites/genenames.org/files/documents/PMID16284797.pdf>`_
- Eyre TA, Wright MW, Lush MJ and Bruford EA.
    HCOP: a searchable database of human orthology predictions.
    Brief Bioinform. 2007 Jan;8(1):2-5. PMID:
    `16951416 <https://www.ncbi.nlm.nih.gov/pubmed/16951416>`_
- Gray KA, Yates, B, Seal RL, Wright MW, Bruford EA.
    Genenames.org: the HGNC resources in 2015.
    Nucleic Acids Res. 2015 Jan;43(Database issue):D1079-85. PMID:
    `25361968 <http://www.ncbi.nlm.nih.gov/pubmed/25361968>`_

Links
-----

- `HCOP: Orthology Predictions Search <http://www.genenames.org/cgi-bin/hcop>`_
