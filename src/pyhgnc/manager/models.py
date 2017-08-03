"""This file contains the relational database models used by PyWikiPathways to store information from WikiPathways."""

from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

HGNC_TABLE_NAME = 'pyhgnc_hgnc'
ALIASSYMBOL_TABLE_NAME = 'pyhgnc_alassymbol'
ALIASNAME_TABLE_NAME = 'pyhgnc_aliasname'
GENEFAMILY_TABLE_NAME = 'pyhgnc_genefamily'
REFSEQ_TABLE_NAME = 'pyhgnc_refseqaccession'
RGD_TABLE_NAME = 'pyhgnc_rgd'
OMIM_TABLE_NAME = 'pyhgnc_omim'
MGD_TABLE_NAME = 'pyhgnc_mgd'
UNIPROT_TABLE_NAME = 'pyhgnc_uniprot'
CCDS_TABLE_NAME = 'pyhgnc_ccds'
PUBMED_TABLE_NAME = 'pyhgnc_pubmed'
ENA_TABLE_NAME = 'pyhgnc_ena'
ENZYME_TABLE_NAME = 'pyhgnc_enzyme'
LSDB_TABLE_NAME = 'pyhgnc_lsdb'

Base = declarative_base()


class HGNC(Base):
    __tablename__ = HGNC_TABLE_NAME

    id = Column(Integer, primary_key=True)

    name = Column(String(255), nullable=True)
    symbol = Column(String(255), index=True)
    hgncID = Column(String(255))
    status = Column(String(255))
    uuid = Column(String(255))

    locusGroup = Column(String(255))
    locusType = Column(String(255))

    # Date information
    datenamechanged = Column(Date, nullable=True)
    datemodified = Column(Date, nullable=True)
    datesymbolchanged = Column(Date, nullable=True)
    dateapprovedreserved = Column(Date, nullable=True)

    # Possible foreign keys ??
    ensemblgene_id = Column(String(255), nullable=True)
    # ToDo: Must this be txt?
    horde_id = Column(Text, nullable=True)
    vega_id = Column(String(255), nullable=True)
    lncrnadb_id = Column(String(255), nullable=True)
    entrez_id = Column(String(255), nullable=True)
    mirbase_id = Column(String(255), nullable=True)
    iuphar_id = Column(String(255), nullable=True)
    ucsc_id = Column(String(255), nullable=True)
    snornabase_id = Column(String(255), nullable=True)
    intermediatefilamentdb_id = Column(String(255), nullable=True)

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
    genefamilies = relationship('GeneFamily')
    refseqaccessions = relationship('RefSeq')
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


class AliasSymbol(Base):
    """Contains all alias symbols and/or previous symbols of an hgnc entry."""
    __tablename__ = ALIASSYMBOL_TABLE_NAME

    id = Column(Integer, primary_key=True)

    symbol = Column(String(255))
    hgnc_id = Column(Integer, ForeignKey('{}.id'.format(HGNC_TABLE_NAME)))
    hgnc = relationship('HGNC', back_populates='symbols')

    isprev = Column(Boolean, default=False)


class AliasName(Base):
    """Contains all alias names and/or previous names of an hgnc entry."""
    __tablename__ = ALIASNAME_TABLE_NAME

    id = Column(Integer, primary_key=True)

    name = Column(String(255))
    hgnc_id = Column(Integer, ForeignKey('{}.id'.format(HGNC_TABLE_NAME)))
    hgnc = relationship('HGNC', back_populates='names')

    isprev = Column(Boolean, default=False)


class GeneFamily(Base):
    """Contains all gene family identifiers and names of an hgnc entry."""
    __tablename__ = GENEFAMILY_TABLE_NAME

    id = Column(Integer, primary_key=True)

    familyid = Column(Integer, nullable=True)
    familyname = Column(String(255), nullable=True)
    hgnc_id = Column(Integer, ForeignKey('{}.id'.format(HGNC_TABLE_NAME)))
    hgnc = relationship('HGNC', back_populates='genefamilies')


class RefSeq(Base):
    __tablename__ = REFSEQ_TABLE_NAME

    id = Column(Integer, primary_key=True)
    accession = Column(String(255))

    hgnc_id = Column(Integer, ForeignKey('{}.id'.format(HGNC_TABLE_NAME)))
    hgnc = relationship('HGNC', back_populates='refseqaccessions')


class RGD(Base):
    __tablename__ = RGD_TABLE_NAME

    id = Column(Integer, primary_key=True)
    rgdid = Column(String(255))

    hgnc_id = Column(Integer, ForeignKey('{}.id'.format(HGNC_TABLE_NAME)))
    hgnc = relationship('HGNC', back_populates='rgds')


class OMIM(Base):
    __tablename__ = OMIM_TABLE_NAME

    id = Column(Integer, primary_key=True)
    omimid = Column(String(255))

    hgnc_id = Column(Integer, ForeignKey('{}.id'.format(HGNC_TABLE_NAME)))
    hgnc = relationship('HGNC', back_populates='omims')


class MGD(Base):
    __tablename__ = MGD_TABLE_NAME

    id = Column(Integer, primary_key=True)
    mgdid = Column(String(255))

    hgnc_id = Column(Integer, ForeignKey('{}.id'.format(HGNC_TABLE_NAME)))
    hgnc = relationship('HGNC', back_populates='mgds')


class Uniprot(Base):
    __tablename__ = UNIPROT_TABLE_NAME

    id = Column(Integer, primary_key=True)
    uniprotid = Column(String(255))

    hgnc_id = Column(Integer, ForeignKey('{}.id'.format(HGNC_TABLE_NAME)))
    hgnc = relationship('HGNC', back_populates='uniprots')


class CCDS(Base):
    __tablename__ = CCDS_TABLE_NAME

    id = Column(Integer, primary_key=True)
    ccdsid = Column(String(255))

    hgnc_id = Column(Integer, ForeignKey('{}.id'.format(HGNC_TABLE_NAME)))
    hgnc = relationship('HGNC', back_populates='ccds')


class PubMed(Base):
    __tablename__ = PUBMED_TABLE_NAME

    id = Column(Integer, primary_key=True)
    pubmedid = Column(String(255))

    hgnc_id = Column(Integer, ForeignKey('{}.id'.format(HGNC_TABLE_NAME)))
    hgnc = relationship('HGNC', back_populates='pubmeds')


class ENA(Base):
    __tablename__ = ENA_TABLE_NAME

    id = Column(Integer, primary_key=True)
    enaid = Column(String(255))

    hgnc_id = Column(Integer, ForeignKey('{}.id'.format(HGNC_TABLE_NAME)))
    hgnc = relationship('HGNC', back_populates='enas')


class Enzyme(Base):
    __tablename__ = ENZYME_TABLE_NAME

    id = Column(Integer, primary_key=True)
    enzymeid = Column(String(255))

    hgnc_id = Column(Integer, ForeignKey('{}.id'.format(HGNC_TABLE_NAME)))
    hgnc = relationship('HGNC', back_populates='enzymes')


class LSDB(Base):
    __tablename__ = LSDB_TABLE_NAME

    id = Column(Integer, primary_key=True)
    lsdb = Column(String(255))

    hgnc_id = Column(Integer, ForeignKey('{}.id'.format(HGNC_TABLE_NAME)))
    hgnc = relationship('HGNC', back_populates='lsdbs')
