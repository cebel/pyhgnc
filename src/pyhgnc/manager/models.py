"""This file contains the relational database models used by HGNC."""

import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean, Date, Table
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship

from .defaults import TABLE_PREFIX

Base = declarative_base()


def foreign_key_to(table_name):
    """Creates a standard foreign key to a table in the database

    :param table_name: name of the table without TABLE_PREFIX
    :type table_name: str
    :return: foreign key column
    :rtype: sqlalchemy.Column
    """
    foreign_column = TABLE_PREFIX + table_name + '.id'
    return Column(Integer, ForeignKey(foreign_column))


def get_many2many_table(table1, table2):
    table_name = ('{}{}__{}'.format(TABLE_PREFIX, table1, table2))
    return Table(table_name, Base.metadata,
                 Column('{}_id'.format(table1), Integer, ForeignKey('{}{}.id'.format(TABLE_PREFIX, table1))),
                 Column('{}_id'.format(table2), Integer, ForeignKey('{}{}.id'.format(TABLE_PREFIX, table2)))
                 )


class MasterModel(object):
    """This class is the parent class of all models in PyHGNC. Automatic creation of table name by class name with
    project prefix"""

    @declared_attr
    def __tablename__(self):
        return TABLE_PREFIX + self.__name__.lower()

    __mapper_args__ = {'always_refresh': True}

    id = Column(Integer, primary_key=True)

    def _to_dict(self):
        data_dict = self.__dict__.copy()
        del data_dict['_sa_instance_state']
        del data_dict['id']
        for k, v in data_dict.items():
            if isinstance(v, datetime.date):
                data_dict[k] = data_dict[k].strftime('%Y-%m-%d')
        return data_dict

    def to_dict(self):
        return self._to_dict()

    def to_dict_with_hgnc(self):
        ret_dict = self._to_dict()
        del ret_dict['hgnc_id']
        ret_dict['hgnc_identifier'] = self.hgnc.identifier
        ret_dict['hgnc_symbol'] = self.hgnc.symbol
        return ret_dict

    def to_dict_with_hgncs(self):
        ret_dict = self._to_dict()
        # ret_dict['hgnc_identifier'] = self.hgnc.identifier
        ret_dict['hgnc_symbols'] = [x.symbol for x in self.hgncs]
        return ret_dict

hgnc_enzyme = get_many2many_table('hgnc', 'enzyme')

hgnc_gene_family = get_many2many_table('hgnc', 'genefamily')

hgnc_refseq = get_many2many_table('hgnc', 'refseq')

hgnc_mgd = get_many2many_table('hgnc', 'mgd')

hgnc_pubmed = get_many2many_table('hgnc', 'pubmed')

hgnc_ena = get_many2many_table('hgnc', 'ena')

hgnc_uniprot = get_many2many_table('hgnc', 'uniprot')

hgnc_rgd = get_many2many_table('hgnc', 'rgd')


class HGNC(Base, MasterModel):
    """Root class (table, model) for all other classes (tables, models) in PyHGNC. Basic information with 1:1
    relationship to identifier are stored here

    .. warning::

        - homeodb (Homeobox Database ID)
        - horde_id (Symbol used within HORDE for the gene)
        described in
        `README <ftp://ftp.ebi.ac.uk/pub/databases/genenames/README.txt>`_, but not found in
        `HGNC JSON file <ftp://ftp.ebi.ac.uk/pub/databases/genenames/new/json/hgnc_complete_set.json>`_

    .. hint::

        To link to IUPHAR/BPS Guide to PHARMACOLOGY database only use the number (only use 1 from the result objectId:1)


    :cvar str name: HGNC approved name for the gene. Equates to the "APPROVED NAME" field within the gene symbol report
    :cvar str symbol: The HGNC approved gene symbol. Equates to the "APPROVED SYMBOL" field within the gene symbol
                        report.
    :cvar int orphanet: Orphanet ID
    :cvar str identifier: HGNC ID. A unique ID created by the HGNC for every approved symbol
    :cvar str status: Status of the symbol report, which can be either "Approved" or "Entry Withdrawn"
    :cvar str uuid: universally unique identifier

    :cvar str locus_group: group name for a set of related locus types as defined by the HGNC (e.g. non-coding RNA).
    :cvar str locus_type: locus type as defined by the HGNC (e.g. RNA, transfer)

    :cvar date date_name_changed: date the gene name was last changed
    :cvar date date_modified: date the entry was last modified
    :cvar date date_symbol_changed: date the gene symbol was last changed
    :cvar date date_approved_reserved: date the entry was first approved

    :cvar str ensembl_gene: Ensembl gene ID. Found within the "GENE RESOURCES" section of the gene symbol report
    :cvar str horde: symbol used within HORDE for the gene (not available in JSON)
    :cvar str vega: Vega gene ID. Found within the "GENE RESOURCES" section of the gene symbol report
    :cvar str lncrnadb: Long Noncoding RNA Database identifier
    :cvar str entrez: Entrez gene ID. Found within the "GENE RESOURCES" section of the gene symbol report
    :cvar str mirbase: miRBase ID
    :cvar str iuphar: The objectId used to link to the IUPHAR/BPS Guide to PHARMACOLOGY database
    :cvar str ucsc: UCSC gene ID. Found within the "GENE RESOURCES" section of the gene symbol report
    :cvar str snornabase: snoRNABase ID
    :cvar str imgt: Symbol used within international ImMunoGeneTics information system

    :cvar str pseudogeneorg: Pseudogene.org ID
    :cvar str bioparadigmsslc: Symbol used to link to the SLC tables database at bioparadigms.org for the gene
    :cvar str locationsortable: locations sortable
    :cvar str merops: ID used to link to the MEROPS peptidase database

    :cvar str location: Cytogenetic location of the gene (e.g. 2q34).
    :cvar str cosmic: Symbol used within the Catalogue of somatic mutations in cancer for the gene


    :cvar list rgds: relationship to `RGD <#rgd>`__
    :cvar list omims: relationship to OMIM
    :cvar list ccdss: relationship to CCDS
    :cvar list lsdbs: relationship to LSDB
    :cvar list orthology_predictions: relationship to OrthologyPrediction

    :cvar list enzymes: relationship to Enzyme
    :cvar list gene_families: relationship to GeneFamily
    :cvar list refseq_accessions: relationship to RefSeq
    :cvar list mgds: relationship to MGD
    :cvar list uniprots: relationship to UniProt
    :cvar list pubmeds: relationship to PubMed
    :cvar list enas: relationship to ENA
    """
    name = Column(String(255), nullable=True)
    symbol = Column(String(255), index=True)
    identifier = Column(Integer, unique=True)
    status = Column(String(255))
    uuid = Column(String(255))
    orphanet = Column(Integer, nullable=True)

    locus_group = Column(String(255))
    locus_type = Column(String(255))

    # Date information
    date_name_changed = Column(Date, nullable=True)
    date_modified = Column(Date, nullable=True)
    date_symbol_changed = Column(Date, nullable=True)
    date_approved_reserved = Column(Date, nullable=True)

    ensembl_gene = Column(String(255), nullable=True)
    horde = Column(String(255), nullable=True)
    vega = Column(String(255), nullable=True)
    lncrnadb = Column(String(255), nullable=True)
    entrez = Column(String(255), nullable=True)
    mirbase = Column(String(255), nullable=True)
    iuphar = Column(String(255), nullable=True)
    ucsc = Column(String(255), nullable=True)
    snornabase = Column(String(255), nullable=True)
    pseudogeneorg = Column(String(255), nullable=True)
    bioparadigmsslc = Column(String(255), nullable=True)
    locationsortable = Column(String(255), nullable=True)
    merops = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    cosmic = Column(String(255), nullable=True)
    imgt = Column(String(255), nullable=True)

    alias_symbols = relationship('AliasSymbol')
    alias_names = relationship('AliasName')
    omims = relationship('OMIM')
    ccdss = relationship('CCDS')
    lsdbs = relationship('LSDB')
    orthology_predictions = relationship('OrthologyPrediction')

    enzymes = relationship(
        "Enzyme",
        secondary=hgnc_enzyme,
        back_populates="hgncs"
    )

    gene_families = relationship(
        'GeneFamily',
        secondary=hgnc_gene_family,
        back_populates="hgncs"
    )

    refseqs = relationship(
        'RefSeq',
        secondary=hgnc_refseq,
        back_populates="hgncs"
    )

    mgds = relationship(
        'MGD',
        secondary=hgnc_mgd,
        back_populates="hgncs"
    )

    pubmeds = relationship(
        'PubMed',
        secondary=hgnc_pubmed,
        back_populates="hgncs"
    )

    enas = relationship(
        'ENA',
        secondary=hgnc_ena,
        back_populates="hgncs"
    )

    uniprots = relationship(
        'UniProt',
        secondary=hgnc_uniprot,
        back_populates="hgncs"
    )

    rgds = relationship(
        'RGD',
        secondary=hgnc_rgd,
        back_populates="hgncs"
    )

    def __repr__(self):
        return self.symbol


class AliasSymbol(Base, MasterModel):
    """Other symbols used to refer to this gene as seen in the "SYNONYMS" field in the symbol report.

    .. attention::

        Symbols previously approved by the HGNC for this
        gene are tagged with `is_previous_symbol==True`. Equates to the "PREVIOUS SYMBOLS & NAMES" field
        within the gene symbol report.

    :cvar str alias_symbol: other symbol
    :cvar bool is_previous_symbol: previously approved
    :cvar hgnc: back populates to :class:`.HGNC`
    """

    alias_symbol = Column(String(255))
    is_previous_symbol = Column(Boolean, default=False)

    hgnc_id = foreign_key_to('hgnc')
    hgnc = relationship('HGNC', back_populates='alias_symbols')

    def to_dict(self):
        return self.to_dict_with_hgnc()

    def __repr__(self):
        return self.alias_symbol


class AliasName(Base, MasterModel):
    """Other names used to refer to this gene as seen in the "SYNONYMS" field in the gene symbol report.

    .. attention::

        Gene names previously approved by the HGNC for this
        gene are tagged with `is_previous_name==True`.. Equates to the "PREVIOUS SYMBOLS & NAMES" field
        within the gene symbol report.

    :cvar str alias_name: other name
    :cvar bool is_previous_name: previously approved
    :cvar hgnc: back populates to :class:`.HGNC`
    """
    alias_name = Column(String(255))
    is_previous_name = Column(Boolean, default=False)

    hgnc_id = foreign_key_to('hgnc')
    hgnc = relationship('HGNC', back_populates='alias_names')

    def to_dict(self):
        return self.to_dict_with_hgnc()

    def __repr__(self):
        return '{}; is_previous:{}'.format(self.alias_name, self.is_previous_name)


class GeneFamily(Base, MasterModel):
    """Name and identifier given to a gene family or group the gene has been assigned to.
    Equates to the "GENE FAMILY" field within
    the gene symbol report.


    :cvar int familyid: family identifier
    :cvar str familyname: family name
    :cvar list hgncs: back populates to :class:`.HGNC`
    """

    family_identifier = Column(Integer, unique=True)
    family_name = Column(String(255))

    hgncs = relationship(
        "HGNC",
        secondary=hgnc_gene_family,
        back_populates="gene_families"
    )

    def to_dict(self):
        return self.to_dict_with_hgncs()

    def __repr__(self):
        return self.family_name


class RefSeq(Base, MasterModel):
    """RefSeq nucleotide accession(s). Found within the"NUCLEOTIDE SEQUENCES" section of the gene symbol report

    See also `RefSeq database <https://www.ncbi.nlm.nih.gov/refseq/>`_ for more information

    :cvar str accession: RefSeq accession number
    :cvar list hgncs: back populates to :class:`.HGNC`
    """
    accession = Column(String(255))

    hgncs = relationship(
        "HGNC",
        secondary=hgnc_refseq,
        back_populates="refseqs"
    )

    def to_dict(self):
        return self.to_dict_with_hgncs()

    def __repr__(self):
        return self.accession


class RGD(Base, MasterModel):
    """Rat genome database gene ID. Found within the "HOMOLOGS" section of the gene symbol report

    :cvar str rgdid: Rat genome database gene ID
    :cvar hgncs: back populates to :class:`.HGNC`
    """
    rgdid = Column(Integer)

    hgncs = relationship(
        "HGNC",
        secondary=hgnc_rgd,
        back_populates="rgds"
    )

    def to_dict(self):
        return self.to_dict_with_hgncs()

    def __repr__(self):
        return str(self.rgdid)


class OMIM(Base, MasterModel):
    """Online Mendelian Inheritance in Man (OMIM) ID

    :cvar str omimid: OMIM ID
    :cvar hgnc: back populates to `pyhgnc.manager.models.HGNC`
    """
    omimid = Column(Integer)

    hgnc_id = foreign_key_to('hgnc')
    hgnc = relationship('HGNC', back_populates='omims')

    def to_dict(self):
        return self.to_dict_with_hgnc()

    def __repr__(self):
        return str(self.omimid)


class MGD(Base, MasterModel):
    """Mouse genome informatics database ID. Found within the "HOMOLOGS" section of the gene symbol report

    :cvar str mgdid: Mouse genome informatics database ID
    :cvar list hgncs: back populates to :class:`.HGNC`
    """
    mgdid = Column(Integer)

    hgncs = relationship(
        "HGNC",
        secondary=hgnc_mgd,
        back_populates="mgds"
    )

    def to_dict(self):
        return self.to_dict_with_hgncs()

    def __repr__(self):
        return str(self.mgdid)


class UniProt(Base, MasterModel):
    """Universal Protein Resource (UniProt) protein accession.
    Found within the "PROTEIN RESOURCES" section of the gene symbol report

    .. note::

        use `pip install pyhgnc` to install PyHGNC Python library from Fraunhofer SCAI BIO

    :cvar str uniprotid: UniProt identifier
    :cvar list hgncs: back populates to :class:`.HGNC`

    see also `UniProt webpage <http://www.uniprot.org>`_ for more information
    """

    uniprotid = Column(String(255))

    hgncs = relationship(
        "HGNC",
        secondary=hgnc_uniprot,
        back_populates="uniprots"
    )

    def to_dict(self):
        return self.to_dict_with_hgncs()

    def __repr__(self):
        return self.uniprotid


class CCDS(Base, MasterModel):
    """Consensus CDS ID. Found within the "NUCLEOTIDE SEQUENCES" section of the gene symbol report

    see also `CCDS <https://www.ncbi.nlm.nih.gov/projects/CCDS>`_ for more information

    :cvar str ccdsid: CCDS identifier
    :cvar hgnc: back populates to :class:`.HGNC`

    """
    ccdsid = Column(String(255))

    hgnc_id = foreign_key_to('hgnc')
    hgnc = relationship('HGNC', back_populates='ccdss')

    def to_dict(self):
        return self.to_dict_with_hgnc()

    def __repr__(self):
        return self.ccdsid


class PubMed(Base, MasterModel):
    """Pubmed and Europe Pubmed Central PMID

    :cvar str pubmedid: Pubmed identifier
    :cvar list hgncs: back populates to :class:`.HGNC`
    """
    pubmedid = Column(Integer)

    hgncs = relationship(
        "HGNC",
        secondary=hgnc_pubmed,
        back_populates="pubmeds"
    )

    def to_dict(self):
        return self.to_dict_with_hgncs()

    def __repr__(self):
        return str(self.pubmedid)


class ENA(Base, MasterModel):
    """International Nucleotide Sequence Database Collaboration (GenBank, ENA and DDBJ) accession
    number(s). Found within the "NUCLEOTIDE SEQUENCES" section of the gene symbol report.

    :cvar str enaid: European Nucleotide Archive (ENA) identifier
    :cvar list hgncs: back populates to :class:`.HGNC`
    """

    enaid = Column(String(255))

    hgncs = relationship(
        "HGNC",
        secondary=hgnc_ena,
        back_populates="enas"
    )

    def to_dict(self):
        return self.to_dict_with_hgncs()

    def __repr__(self):
        return self.enaid


class Enzyme(Base, MasterModel):
    """Enzyme Commission number (EC number)

    :cvar str ec_number: EC number
    :cvar list hgncs: back populates to :class:`.HGNC`
    """

    ec_number = Column(String(255))

    hgncs = relationship(
        "HGNC",
        secondary=hgnc_enzyme,
        back_populates="enzymes"
    )

    def to_dict(self):
        return self.to_dict_with_hgncs()

    def __repr__(self):
        return self.ec_number


class LSDB(Base, MasterModel):
    """The name of the Locus Specific Mutation Database and URL

    :cvar str lsdb: name of the Locus Specific Mutation Database
    :cvar str url: URL to database
    :cvar hgnc: back populates to :class:`.HGNC`
    """

    lsdb = Column(String(255))
    url = Column(Text)

    hgnc_id = foreign_key_to('hgnc')
    hgnc = relationship('HGNC', back_populates='lsdbs')

    def to_dict(self):
        return self.to_dict_with_hgnc()

    def __repr__(self):
        return self.lsdb


class OrthologyPrediction(Base, MasterModel):
    """Orthology Predictions

    .. warning::

        OrthologyPrediction is still not correctly normalized and documented.

    :cvar int ortholog_species: NCBI taxonomy identifier
    :cvar int human_entrez_gene: Human Entrey gene identifier
    :cvar str human_ensembl_gene: Human Ensembl gene identifier
    :cvar str human_name: Human gene name
    :cvar str human_symbol: Human gene symbol
    :cvar str human_chr: Human gene chromosome location
    :cvar str human_assert_ids:
    :cvar str ortholog_species_entrez_gene: Ortholog species Entrez gene identifier
    :cvar str ortholog_species_ensembl_gene: Ortholog species Ensembl gene identifier
    :cvar str ortholog_species_db_id: Ortholog species database identifier
    :cvar str ortholog_species_name: Ortholog species gene name
    :cvar str ortholog_species_symbol: Ortholog species gene symbol
    :cvar str ortholog_species_chr: Ortholog species gene chromosome location
    :cvar str ortholog_species_assert_ids:
    :cvar str support:
    :cvar hgnc: back populates to :class:`.HGNC`

    """
    ortholog_species = Column(Integer)
    human_entrez_gene = Column(Integer)
    human_ensembl_gene = Column(String(255))
    human_name = Column(String(255))
    human_symbol = Column(String(255))
    human_chr = Column(String(255))
    human_assert_ids = Column(String(255))
    ortholog_species_entrez_gene = Column(Integer)
    ortholog_species_ensembl_gene = Column(String(255))
    ortholog_species_db_id = Column(String(255))
    ortholog_species_name = Column(Text)
    ortholog_species_symbol = Column(String(255))
    ortholog_species_chr = Column(String(255))
    ortholog_species_assert_ids = Column(String(255))
    support = Column(String(255))

    hgnc_id = foreign_key_to('hgnc')
    hgnc = relationship('HGNC', back_populates='orthology_predictions')

    def to_dict(self):
        return self.to_dict_with_hgnc()

    def __repr__(self):
        return '{}: {}: {}'.format(self.ortholog_species, self.ortholog_species_name, self.ortholog_species_symbol)


class AppUser(Base, MasterModel):
    name = Column(String(255))
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True)
    password = Column(String(255))

    def __repr__(self):
        return self.username
