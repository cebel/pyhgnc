"""This file contains the relational database models used by HGNC."""

from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean, Date
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
    symbols = relationship('AliasSymbol')
    names = relationship('AliasName')
    gene_families = relationship('GeneFamily')
    refseq_accessions = relationship('RefSeq')
    mgds = relationship('MGD')
    rgds = relationship('RGD')
    omims = relationship('OMIM')
    uniprots = relationship('Uniprot')
    ccds = relationship('CCDS')
    pubmeds = relationship('PubMed')
    enas = relationship('ENA')
    enzymes = relationship('Enzyme')
    lsdbs = relationship('LSDB')

    # cd = models.TextField(null=True)


class AliasSymbol(Base, MasterModel):
    """Contains all alias symbols and/or previous symbols of an hgnc entry.

    :cvar str symbol:
    :cvar bool isprev:
    """

    symbol = Column(String(255))

    hgnc_id = foreign_key_to('hgnc')
    hgnc = relationship('HGNC', back_populates='symbols')

    isprev = Column(Boolean, default=False)


class AliasName(Base, MasterModel):
    """Contains all alias names and/or previous names of an hgnc entry.

    :cvar str name:
    :cvar bool isprev:
    """
    name = Column(String(255))

    hgnc_id = foreign_key_to('hgnc')
    hgnc = relationship('HGNC', back_populates='names')

    isprev = Column(Boolean, default=False)


class GeneFamily(Base, MasterModel):
    """Contains all gene family identifiers and names of an hgnc entry.

    :cvar int familyid:
    :cvar str familyname:
    """

    familyid = Column(Integer, nullable=True)
    familyname = Column(String(255), nullable=True)

    hgnc_id = foreign_key_to('hgnc')
    hgnc = relationship('HGNC', back_populates='gene_families')


class RefSeq(Base, MasterModel):
    """RefSeq accession number

    See also `RefSeq database <https://www.ncbi.nlm.nih.gov/refseq/>`_ for more information

    :cvar str accession:
    """
    accession = Column(String(255))

    hgnc_id = foreign_key_to('hgnc')
    hgnc = relationship('HGNC', back_populates='refseq_accessions')


class RGD(Base, MasterModel):
    """Rat Genome Database identifier

    :cvar str rgdid:
    """
    rgdid = Column(String(255))

    hgnc_id = foreign_key_to('hgnc')
    hgnc = relationship('HGNC', back_populates='rgds')


class OMIM(Base, MasterModel):
    """Online Mendelian Inheritance in Man identifier

    :cvar str omimid:
    """
    omimid = Column(String(255))

    hgnc_id = foreign_key_to('hgnc')
    hgnc = relationship('HGNC', back_populates='omims')


class MGD(Base, MasterModel):
    """Mouse Genome Database identifier

    :cvar str mgdid:
    """
    mgdid = Column(String(255))

    hgnc_id = foreign_key_to('hgnc')
    hgnc = relationship('HGNC', back_populates='mgds')


class Uniprot(Base, MasterModel):
    """Universal Protein Resource (UniProt) identifier

    :cvar str uniprotid:

    see also `UniProt webpage <http://www.uniprot.org>`_ for more information
    """

    uniprotid = Column(String(255))

    hgnc_id = foreign_key_to('hgnc')
    hgnc = relationship('HGNC', back_populates='uniprots')


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
    pubmedid = Column(String(255))

    hgnc_id = foreign_key_to('hgnc')
    hgnc = relationship('HGNC', back_populates='pubmeds')


class ENA(Base, MasterModel):
    """European Nucleotide Archive (ENA) identifier

    :cvar str enaid:
    """

    enaid = Column(String(255))

    hgnc_id = foreign_key_to('hgnc')
    hgnc = relationship('HGNC', back_populates='enas')


class Enzyme(Base, MasterModel):
    """Enzyme identifier

    :cvar str enzymeid:
    """

    enzymeid = Column(String(255))

    hgnc_id = foreign_key_to('hgnc')
    hgnc = relationship('HGNC', back_populates='enzymes')


class LSDB(Base, MasterModel):
    """Locus Specific Mutation Database

    :cvar str lsdb:
    """

    lsdb = Column(String(255))

    hgnc_id = foreign_key_to('hgnc')
    hgnc = relationship('HGNC', back_populates='lsdbs')
