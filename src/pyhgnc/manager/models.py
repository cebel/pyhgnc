"""This file contains the relational database models used by HGNC."""

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

    @declared_attr
    def __tablename__(self):
        return TABLE_PREFIX + self.__name__.lower()

    __mapper_args__ = {'always_refresh': True}

    id = Column(Integer, primary_key=True)

    def to_json(self):
        data_dict = self.__dict__.copy()
        del data_dict['_sa_instance_state']
        return data_dict

hgnc_enzyme = get_many2many_table('hgnc', 'enzyme')

hgnc_gene_family = get_many2many_table('hgnc', 'genefamily')

hgnc_refseq = get_many2many_table('hgnc', 'refseq')

hgnc_mgd = get_many2many_table('hgnc', 'mgd')

hgnc_uniprot = get_many2many_table('hgnc', 'uniprot')

hgnc_pubmed = get_many2many_table('hgnc', 'pubmed')

hgnc_ena =  get_many2many_table('hgnc', 'ena')


class HGNC(Base, MasterModel):
    """
    :cvar str name:
    :cvar str symbol:
    :cvar str identifier:
    :cvar str status:
    :cvar str uuid:

    :cvar str locus_group:
    :cvar str locus_type:

    :cvar date date_name_changed:
    :cvar date date_modified:
    :cvar date date_symbol_changed:
    :cvar date date_approved_reserved:

    :cvar str ensembl_gene:
    :cvar str horde:
    :cvar str vega:
    :cvar str lncrnadb:
    :cvar str entrez:
    :cvar str mirbase:
    :cvar str iuphar:
    :cvar str ucsc:
    :cvar str snornabase:
    :cvar str intermediatefilamentdb:

    :cvar str pseudogeneorg:
    :cvar str bioparadigmsslc:
    :cvar str locationsortable:
    :cvar str merop:

    :cvar str location:
    :cvar str cosmic:
    """
    name = Column(String(255), nullable=True)
    symbol = Column(String(255), index=True)
    identifier = Column(Integer)
    status = Column(String(255))
    uuid = Column(String(255))

    locus_group = Column(String(255))
    locus_type = Column(String(255))

    # Date information
    date_name_changed = Column(Date, nullable=True)
    date_modified = Column(Date, nullable=True)
    date_symbol_changed = Column(Date, nullable=True)
    date_approved_reserved = Column(Date, nullable=True)

    # Possible foreign keys ??
    ensembl_gene = Column(String(255), nullable=True)
    # ToDo: Must this be txt?
    horde = Column(Text, nullable=True)
    vega = Column(String(255), nullable=True)
    lncrnadb = Column(String(255), nullable=True)
    entrez = Column(String(255), nullable=True)
    mirbase = Column(String(255), nullable=True)
    iuphar = Column(String(255), nullable=True)
    ucsc = Column(String(255), nullable=True)
    snornabase = Column(String(255), nullable=True)
    intermediatefilamentdb = Column(String(255), nullable=True)

    pseudogeneorg = Column(String(255), nullable=True)
    bioparadigmsslc = Column(String(255), nullable=True)
    locationsortable = Column(String(255), nullable=True)
    merop = Column(String(255), nullable=True)

    location = Column(String(255), nullable=True)
    cosmic = Column(String(255), nullable=True)

    # ToDo: Must this be txt?
    imgt = Column(Text, nullable=True)

    # Boolean identifiers of several parameters (relationships)
    alias_symbols = relationship('AliasSymbol')
    alias_names = relationship('AliasName')


    rgds = relationship('RGD')
    omims = relationship('OMIM')

    ccds = relationship('CCDS')

    lsdbs = relationship('LSDB')

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

    refseq_accessions = relationship(
        'RefSeq',
        secondary=hgnc_refseq,
        back_populates="hgncs"
    )

    mgds = relationship(
        'MGD',
        secondary=hgnc_mgd,
        back_populates="hgncs"
    )

    uniprots = relationship(
        'Uniprot',
        secondary=hgnc_uniprot,
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

    # cd = models.TextField(null=True)


class AliasSymbol(Base, MasterModel):
    """Contains all alias symbols and/or previous symbols of an hgnc entry.

    :cvar str symbol:
    :cvar bool isprev:
    """

    alias_symbol = Column(String(255))

    hgnc_id = foreign_key_to('hgnc')
    hgnc = relationship('HGNC', back_populates='alias_symbols')

    isprev = Column(Boolean, default=False)


class AliasName(Base, MasterModel):
    """Contains all alias names and/or previous names of an hgnc entry.

    :cvar str name:
    :cvar bool isprev:
    """
    alias_name = Column(String(255))

    hgnc_id = foreign_key_to('hgnc')
    hgnc = relationship('HGNC', back_populates='alias_names')

    isprev = Column(Boolean, default=False)


class GeneFamily(Base, MasterModel):
    """Contains all gene family identifiers and names of an hgnc entry.

    :cvar int familyid:
    :cvar str familyname:
    """

    family_identifier = Column(Integer, unique=True)
    family_name = Column(String(255))

    hgncs = relationship(
        "HGNC",
        secondary=hgnc_gene_family,
        back_populates="gene_families")


class RefSeq(Base, MasterModel):
    """RefSeq accession number

    See also `RefSeq database <https://www.ncbi.nlm.nih.gov/refseq/>`_ for more information

    :cvar str accession:
    """
    accession = Column(String(255))

    hgncs = relationship(
        "HGNC",
        secondary=hgnc_refseq,
        back_populates="refseq_accessions")


class RGD(Base, MasterModel):
    """Rat Genome Database identifier

    :cvar str rgdid:
    """
    rgdid = Column(Integer)

    hgnc_id = foreign_key_to('hgnc')
    hgnc = relationship('HGNC', back_populates='rgds')


class OMIM(Base, MasterModel):
    """Online Mendelian Inheritance in Man identifier

    :cvar str omimid:
    """
    omimid = Column(Integer)

    hgnc_id = foreign_key_to('hgnc')
    hgnc = relationship('HGNC', back_populates='omims')


class MGD(Base, MasterModel):
    """Mouse Genome Database identifier

    :cvar str mgdid:
    """
    mgdid = Column(Integer)

    hgncs = relationship(
        "HGNC",
        secondary=hgnc_mgd,
        back_populates="mgds")


class Uniprot(Base, MasterModel):
    """Universal Protein Resource (UniProt) identifier

    :cvar str uniprotid:

    see also `UniProt webpage <http://www.uniprot.org>`_ for more information
    """

    uniprotid = Column(String(255))

    hgncs = relationship(
        "HGNC",
        secondary=hgnc_uniprot,
        back_populates="uniprots")


class CCDS(Base, MasterModel):
    """Consensus CDS (CCDS) project identifier

    see also `CCDS <https://www.ncbi.nlm.nih.gov/projects/CCDS>`_ for more information

    """
    ccdsid = Column(String(255))

    hgnc_id = foreign_key_to('hgnc')
    hgnc = relationship('HGNC', back_populates='ccds')


class PubMed(Base, MasterModel):
    """PubMed identifier

    TODO: pubmedid should be an integer

    :cvar str pubmedid:
    """
    pubmedid = Column(Integer)

    hgncs = relationship(
        "HGNC",
        secondary=hgnc_pubmed,
        back_populates="pubmeds")


class ENA(Base, MasterModel):
    """European Nucleotide Archive (ENA) identifier

    :cvar str enaid:
    """

    enaid = Column(String(255))

    hgncs = relationship(
        "HGNC",
        secondary=hgnc_ena,
        back_populates="enas")


class Enzyme(Base, MasterModel):
    """Enzyme identifier

    :cvar str enzymeid:
    """

    ec_number = Column(String(255))

    hgncs = relationship(
        "HGNC",
        secondary=hgnc_enzyme,
        back_populates="enzymes")


class LSDB(Base, MasterModel):
    """Locus Specific Mutation Database

    :cvar str lsdb:
    """

    lsdb = Column(String(255))

    hgnc_id = foreign_key_to('hgnc')
    hgnc = relationship('HGNC', back_populates='lsdbs')
