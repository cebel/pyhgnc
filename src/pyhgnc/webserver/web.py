from flasgger import Swagger
from functools import wraps
from flask import Flask, jsonify, request, render_template, flash, redirect, url_for, session
from passlib.hash import sha256_crypt
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from ..manager.models import AppUser
from ..manager.query import QueryManager
from .. import __title__ as project_title

app = Flask(__name__)

app.debug = True

swagger_description = """
<table><tr><td>![alt text](../static/images/project_logo.png)</td><td>
This exposes the functions of [PyHGNC](https://pypi.python.org/pypi/pyhgnc) as a RESTful API. PyHGNC is a Python library
which allows to store and query HGNC data in a local database. [HGNC](http://www.genenames.org/) provides 
unique symbols and names for human loci, including protein coding genes, ncRNA genes and pseudogenes. 
Documentation of the software you can find [here](http://pyhgnc.readthedocs.io/en/latest/). PyHGNC
and its RESTful API also allows access to [HGNC Orthology Predictions (HCOP)](http://www.genenames.org/cgi-bin/hcop) 
(predictions from [eggNOG](http://eggnog.embl.de), [Ensembl Compara](http://www.ensembl.org/info/genome/compara), 
[HGNC](http://www.genenames.org), [HomoloGene](https://www.ncbi.nlm.nih.gov/homologene), 
[Inparanoid](http://inparanoid.sbc.su.se), 
[NCBI Gene Orthology](https://www.ncbi.nlm.nih.gov/books/NBK3841/#EntrezGene.General_Gene_Information), 
[OMA](http://omabrowser.org), [OrthoDB](http://www.orthodb.org), [OrthoMCL](http://orthomcl.org/orthomcl), 
[Panther](http://www.pantherdb.org), [PhylomeDB](http://phylomedb.org), [TreeFam](http://www.treefam.org), 
[ZFIN](http://zfin.org)) with the API function **get_api_query_orthology_prediction**.
</td>
</tr></table>
<table><tr>
    <td>![alt text](../static/images/imi_logo.png)</td>
    <td>![alt text](../static/images/aetionomy_logo.png)</td>
    <td>![alt text](../static/images/phago_logo.png)</td>
    <td>![alt text](../static/images/scai_logo.png)</td>
<tr>
"""

app.config.setdefault('SWAGGER', {
    'title': 'PyHGNC Web API',
    'description': swagger_description,
    'contact': {
        'responsibleOrganization': 'Fraunhofer SCAI',
        'responsibleDeveloper': 'Christian Ebeling',
        'email': 'christian.ebeling@scai.fraunhofer.de',
        'url': 'https://www.scai.fraunhofer.de/de/geschaeftsfelder/bioinformatik.html',
    },
    'version': '0.1.0',
})
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

swagger = Swagger(app)
query = QueryManager()


def get_args(request_args, allowed_int_args=(), allowed_str_args=(), allowed_bool_args=()):
    """Check allowed argument names and return is as dictionary"""
    args = {}

    for allowed_int_arg in allowed_int_args:
        int_value = request_args.get(allowed_int_arg, default=None, type=None)

        if int_value:
            args[allowed_int_arg] = int(int_value)

    for allowed_str_arg in allowed_str_args:
        str_value = request_args.get(allowed_str_arg, default=None, type=None)

        if str_value:
            args[allowed_str_arg] = str_value

    for allowed_bool_arg in allowed_bool_args:
        str_value = request_args.get(allowed_bool_arg, default=None, type=None)

        if str_value == 'true':
            args[allowed_bool_arg] = True

        elif str_value == 'false':
            args[allowed_bool_arg] = False

    return args


@app.route("/")
def index():
    return render_template('home.html', project_title=project_title)


# Check if user is logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, please login', 'danger')
            return redirect(url_for('login'))
    return wrap


# About
@app.route('/about')
def about():
    return render_template('about.html')


# Register form class
class RegisterForm(Form):
    name = StringField(u'Name', [validators.Length(min=3, max=50)])
    username = StringField(u'User Name', [validators.Length(min=4, max=25)])
    email = StringField(u'Email', [validators.Length(min=6, max=50)])
    password = PasswordField(u'Password', [
        validators.data_required(),
        validators.equal_to('confirm', message='Password do not match')
    ])
    confirm = PasswordField('Confirm Password')


# User register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():

        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # insert
        query.session.add(AppUser(name=name, email=email, username=username, password=password))
        query.session.flush()

        flash('You are now registered and can login', 'success')

        return redirect(url_for('login'))

    return render_template('register.html', form=form)


# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('Logged out!', 'success')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get form fields
        username = request.form['username']
        password_candidate = request.form['password']

        # get user by username
        user = query.session.query(AppUser).filter(AppUser.username == username).one_or_none()

        if user:
            if sha256_crypt.verify(password_candidate, user.password):
                app.logger.info('PASSWORD matched')
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in!', 'success')

                return redirect(url_for('dashboard'))
            else:
                app.logger.info('PASSWORD NOT matched')
                error = 'Invalid login'
                return render_template('login.html', error=error)
        else:
            app.logger.info('Username not found')
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')


# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    # create cursor
    entries = query.entry(limit=10)

    if len(entries) > 0:
        return render_template('dashboard.html', entries=entries)
    else:
        msg = 'No articles found'
        return render_template('dashboard.html', msg=msg)


@app.route("/api/query/hgnc/", methods=['GET', 'POST'])
def query_entry():
    """
    Returns list of HGNC entries by query paramaters
    ---

    tags:

      - Query functions

    parameters:

      - name: name
        in: query
        type: string
        required: false
        description: 'HGNC approved name for the gene'
        default: 'lysine demethylase 1A'

      - name: symbol
        in: query
        type: string
        required: false
        description: 'HGNC symbol'
        default: KDM1A

      - name: identifier
        in: query
        type: integer
        required: false
        description: 'HGNC ID. A unique ID created by the HGNC for every approved symbol'
        default: 29079

      - name: status
        in: query
        type: string
        required: false
        description: 'Status of the symbol report, which can be either "Approved" or "Entry Withdrawn"'
        default: Approved

      - name: uuid
        in: query
        type: string
        required: false
        description: 'universally unique identifier'
        default: '032998f3-5339-4c36-a521-1960c2f86cee'

      - name: orphanet
        in: query
        type: integer
        required: false
        description: 'Orphanet database identifier'
        default: 478263

      - name: locus_group
        in: query
        type: string
        required: false
        description: 'group name for a set of related locus types as defined by the HGNC'
        default: 'protein-coding gene'

      - name: locus_type
        in: query
        type: string
        required: false
        description: 'locus type as defined by the HGNC'
        default: 'gene with protein product'

      - name: date_name_changed
        in: query
        type: string
        required: false
        description: 'date the gene name was last changed'
        default: '2016-02-12'

      - name: date_modified
        in: query
        type: string
        required: false
        description: 'date the entry was last modified'
        default: '2017-07-07'

      - name: date_symbol_changed
        in: query
        type: string
        required: false
        description: 'date the gene symbol was last changed'
        default: '2009-09-29'

      - name: date_approved_reserved
        in: query
        type: string
        required: false
        description: 'date the entry was first approved'
        default: '2004-02-26'

      - name: ensembl_gene
        in: query
        type: string
        required: false
        description: 'Ensembl gene ID. Found within the "GENE RESOURCES" section of the gene symbol report'
        default: 'ENSG00000004487'

      - name: vega
        in: query
        type: string
        required: false
        description: 'Vega gene ID. Found within the "GENE RESOURCES" section of the gene symbol report'
        default: 'OTTHUMG00000003220'

      - name: lncrnadb
        in: query
        type: string
        required: false
        description: 'Noncoding RNA Database identifier'
        default:

      - name: horde
        in: query
        type: string
        required: false
        description: 'symbol used within HORDE for the gene (not available in JSON)'
        default:

      - name: entrez
        in: query
        type: string
        required: false
        description: 'Entrez gene ID. Found within the "GENE RESOURCES" section of the gene symbol report'
        default: 23028

      - name: mirbase
        in: query
        type: string
        required: false
        description: 'miRBase ID'
        default:

      - name: iuphar
        in: query
        type: string
        required: false
        description: 'The objectId used to link to the IUPHAR/BPS Guide to PHARMACOLOGY database'
        default: 'objectId:2669'

      - name: ucsc
        in: query
        type: string
        required: false
        description: 'UCSC gene ID. Found within the "GENE RESOURCES" section of the gene symbol report'
        default: 'uc001bgi.3'

      - name: snornabase
        in: query
        type: string
        required: false
        description: 'snoRNABase ID'
        default:

      - name: pseudogeneorg
        in: query
        type: string
        required: false
        description: 'Pseudogene.org ID'
        default:

      - name: bioparadigmsslc
        in: query
        type: string
        required: false
        description: 'Symbol used to link to the SLC tables database at bioparadigms.org for the gene'
        default:

      - name: locationsortable
        in: query
        type: string
        required: false
        description: 'locations sortable'
        default: 01p36.12

      - name: merops
        in: query
        type: string
        required: false
        description: 'ID used to link to the MEROPS peptidase database'
        default:

      - name: location
        in: query
        type: string
        required: false
        description: 'Cytogenetic location of the gene (e.g. 2q34)'
        default: 1p36.12

      - name: cosmic
        in: query
        type: string
        required: false
        description: 'Symbol used within the Catalogue of somatic mutations in cancer for the gene'
        default: 'KDM1A'

      - name: imgt
        in: query
        type: string
        required: false
        description: 'Symbol used within international ImMunoGeneTics information system'
        default:

      - name: limit
        in: query
        type: integer
        required: false
        default: 1
    """
    allowed_str_args = ['name', 'symbol', 'status', 'uuid', 'locus_group', 'locus_type',
                        'date_name_changed', 'date_modified', 'date_symbol_changed', 'date_approved_reserved',
                        'ensembl_gene', 'vega', 'lncrnadb', 'horde', 'mirbase', 'iuphar', 'ucsc', 'snornabase',
                        'pseudogeneorg', 'bioparadigmsslc', 'locationsortable', 'merops', 'location', 'cosmic', 'imgt'
                        ]

    allowed_int_args = ['limit', 'identifier', 'orphanet', 'entrez', ]

    args = get_args(
        request_args=request.args,
        allowed_int_args=allowed_int_args,
        allowed_str_args=allowed_str_args
    )

    return jsonify(query.hgnc(**args))


@app.route("/api/query/alias_name/", methods=['GET', 'POST'])
def alias_name():
    """
    Returns list of alias name by query paramaters
    ---

    tags:

      - Query functions

    parameters:

      - name: alias_name
        in: query
        type: string
        required: false
        description: 'Other names used to refer to a gene'
        default: 'peptidase nexin-II'

      - name: is_previous_name
        in: query
        type: boolean
        required: false
        description: 'Other names used to refer to a gene'
        default: false

      - name: hgnc_symbol
        in: query
        type: string
        required: false
        description: 'HGNC symbol'
        default: APP

      - name: hgnc_identifier
        in: query
        type: integer
        required: false
        description: 'HGNC identifier'
        default: 620

      - name: limit
        in: query
        type: integer
        required: false
        default: 1
    """
    allowed_str_args = ['alias_name', 'hgnc_symbol', 'hgnc_identifier']

    allowed_int_args = ['limit', ]

    allowed_bool_args = ['is_previous_name', ]

    args = get_args(
        request_args=request.args,
        allowed_int_args=allowed_int_args,
        allowed_str_args=allowed_str_args,
        allowed_bool_args=allowed_bool_args,
    )

    return jsonify(query.alias_name(**args))


@app.route("/api/query/orthology_prediction/", methods=['GET', 'POST'])
def orthology_prediction():
    """
    Returns list of HGNC entries by query paramaters

    <a href="http://test.de">rst test </a>
    ---

    tags:

      - Query functions

    parameters:

      - name: ortholog_species
        in: query
        type: integer
        required: false
        description: 'NCBI taxonomy identifier'
        default: 10090

      - name: human_entrez_gene
        in: query
        type: integer
        required: false
        description: 'Human Entrey gene identifier'
        default: 351

      - name: human_ensembl_gene
        in: query
        type: string
        required: false
        description: 'Human Ensembl gene identifier'
        default: 'ENSG00000142192'

      - name: human_name
        in: query
        type: string
        required: false
        description: 'Human gene name'
        default: 'amyloid beta precursor protein'

      - name: human_symbol
        in: query
        type: string
        required: false
        description: 'Human gene symbol'
        default: 'APP'

      - name: human_chr
        in: query
        type: string
        required: false
        description: 'Human gene chromosome location'
        default: '21q21.3'

      - name: human_assert_ids
        in: query
        type: string
        required: false
        description: 'human cross references'
        default: '%P05067%'

      - name: ortholog_species_entrez_gene
        in: query
        type: integer
        required: false
        description: 'Ortholog species Entrez gene identifier'
        default: 11820

      - name: ortholog_species_ensembl_gene
        in: query
        type: string
        required: false
        description: 'Ortholog species Ensembl gene identifier'
        default: 'ENSMUSG00000022892'

      - name: ortholog_species_db_id
        in: query
        type: string
        required: false
        description: 'Ortholog species database identifier'
        default: 'MGI:88059'

      - name: ortholog_species_name
        in: query
        type: string
        required: false
        description: 'Ortholog species gene name'
        default: 'amyloid beta (A4) precursor protein'

      - name: ortholog_species_symbol
        in: query
        type: string
        required: false
        description: 'Ortholog species gene symbol'
        default: 

      - name: ortholog_species_chr
        in: query
        type: string
        required: false
        description: 'Ortholog species gene chromosome location'
        default: 16

      - name: ortholog_species_assert_ids
        in: query
        type: string
        required: false
        description: 'ortholog species cross references'
        default: '%P12023%'

      - name: support
        in: query
        type: string
        required: false
        description: 'Support on HGNC website'
        default: '%OrthoDB%'

      - name: hgnc_symbol
        in: query
        type: string
        required: false
        description: 'HGNC symbol'
        default: 'APP'

      - name: hgnc_identifier
        in: query
        type: integer
        required: false
        description: 'HGNC identifier'
        default: 620

      - name: limit
        in: query
        type: integer
        required: false
        default: 1
    """
    allowed_str_args = ['ortholog_species', 'human_entrez_gene', 'human_ensembl_gene', 'human_name', 'human_symbol',
                        'human_chr', 'human_assert_ids', 'ortholog_species_entrez_gene',
                        'ortholog_species_ensembl_gene', 'ortholog_species_db_id', 'ortholog_species_name',
                        'ortholog_species_symbol', 'ortholog_species_chr', 'ortholog_species_assert_ids', 'support',
                        'hgnc_symbol', 'hgnc_identifier']

    allowed_int_args = ['limit', 'ortholog_species']

    args = get_args(
        request_args=request.args,
        allowed_int_args=allowed_int_args,
        allowed_str_args=allowed_str_args
    )

    return jsonify(query.orthology_prediction(**args))


@app.route("/api/query/alias_symbol/", methods=['GET', 'POST'])
def alias_symbol():
    """
    Returns list of alias symbol by query paramaters
    ---

    tags:

      - Query functions

    parameters:

      - name: alias_symbol
        in: query
        type: string
        required: false
        description: 'Other symbols used to refer to a gene'
        default: 'AD1'

      - name: is_previous_symbol
        in: query
        type: boolean
        required: false
        description: 'Other names used to refer to a gene'
        default: true

      - name: hgnc_symbol
        in: query
        type: string
        required: false
        description: 'HGNC symbol'
        default: APP

      - name: hgnc_identifier
        in: query
        type: integer
        required: false
        description: 'HGNC identifier'
        default: 620

      - name: limit
        in: query
        type: integer
        required: false
        default: 1
    """
    allowed_str_args = ['alias_symbol', 'hgnc_symbol', 'hgnc_identifier']

    allowed_int_args = ['limit', ]

    allowed_bool_args = ['is_previous_symbol', ]

    args = get_args(
        request_args=request.args,
        allowed_int_args=allowed_int_args,
        allowed_str_args=allowed_str_args,
        allowed_bool_args=allowed_bool_args,
    )

    return jsonify(query.alias_symbol(**args))


@app.route("/api/query/gene_family/", methods=['GET', 'POST'])
def gene_family():
    """
    Returns list of HGNC entries by query paramaters
    ---

    tags:

      - Query functions

    parameters:

      - name: family_identifier
        in: query
        type: integer
        required: false
        description: 'Gene Family identifier'
        default: 542

      - name: family_name
        in: query
        type: string
        required: false
        description: 'Gene Family name'
        default: 'Endogenous ligands'

      - name: hgnc_symbol
        in: query
        type: string
        required: false
        description: 'HGNC symbol'
        default: 'APP'

      - name: hgnc_identifier
        in: query
        type: integer
        required: false
        description: 'HGNC identifier'
        default: 620

      - name: limit
        in: query
        type: integer
        required: false
        default: 1
    """
    allowed_str_args = ['family_name', 'hgnc_symbol']

    allowed_int_args = ['limit', 'family_identifier', 'hgnc_identifier']

    args = get_args(
        request_args=request.args,
        allowed_int_args=allowed_int_args,
        allowed_str_args=allowed_str_args
    )

    return jsonify(query.gene_family(**args))


@app.route("/api/query/ref_seq/", methods=['GET', 'POST'])
def ref_seq():
    """
    Returns list of RefSeq entries by query paramaters
    ---

    tags:

      - Query functions

    parameters:

      - name: accession
        in: query
        type: string
        required: false
        description: 'RefSeq nucleotide accession'
        default: 'NM_000484'

      - name: hgnc_symbol
        in: query
        type: string
        required: false
        description: 'HGNC symbol'
        default: 'APP'

      - name: hgnc_identifier
        in: query
        type: integer
        required: false
        description: 'HGNC identifier'
        default: 620

      - name: limit
        in: query
        type: integer
        required: false
        default: 1
    """
    allowed_str_args = ['accession', 'hgnc_symbol']

    allowed_int_args = ['limit', 'hgnc_identifier']

    args = get_args(
        request_args=request.args,
        allowed_int_args=allowed_int_args,
        allowed_str_args=allowed_str_args
    )

    return jsonify(query.ref_seq(**args))


@app.route("/api/query/rgd/", methods=['GET', 'POST'])
def rgd():
    """
    Returns list of Rat genome database gene IDs by query paramaters
    ---

    tags:

      - Query functions

    parameters:

      - name: rgdid
        in: query
        type: integer
        required: false
        description: 'Rat genome database gene ID'
        default: 2139

      - name: hgnc_symbol
        in: query
        type: string
        required: false
        description: 'HGNC symbol'
        default: 'APP'

      - name: hgnc_identifier
        in: query
        type: integer
        required: false
        description: 'HGNC identifier'
        default: 620

      - name: limit
        in: query
        type: integer
        required: false
        default: 1
    """
    allowed_str_args = ['hgnc_symbol']

    allowed_int_args = ['rgdid', 'limit', 'hgnc_identifier']

    args = get_args(
        request_args=request.args,
        allowed_int_args=allowed_int_args,
        allowed_str_args=allowed_str_args
    )

    return jsonify(query.rgd(**args))


@app.route("/api/query/omim/", methods=['GET', 'POST'])
def omim():
    """
    Returns list of Online Mendelian Inheritance in Man (OMIM) ID by query paramaters
    ---

    tags:

      - Query functions

    parameters:

      - name: omimid
        in: query
        type: integer
        required: false
        description: 'Online Mendelian Inheritance in Man (OMIM) ID'
        default: 104760

      - name: hgnc_symbol
        in: query
        type: string
        required: false
        description: 'HGNC symbol'
        default: 'APP'

      - name: hgnc_identifier
        in: query
        type: integer
        required: false
        description: 'HGNC identifier'
        default: 620

      - name: limit
        in: query
        type: integer
        required: false
        default: 1
    """
    allowed_str_args = ['hgnc_symbol']

    allowed_int_args = ['omimid', 'limit', 'hgnc_identifier']

    args = get_args(
        request_args=request.args,
        allowed_int_args=allowed_int_args,
        allowed_str_args=allowed_str_args
    )

    return jsonify(query.omim(**args))


@app.route("/api/query/mgd/", methods=['GET', 'POST'])
def mgd():
    """
    Returns list of Mouse genome informatics database ID by query paramaters
    ---

    tags:

      - Query functions

    parameters:

      - name: mgdid
        in: query
        type: integer
        required: false
        description: 'Mouse genome informatics database ID'
        default: 88059

      - name: hgnc_symbol
        in: query
        type: string
        required: false
        description: 'HGNC symbol'
        default: 'APP'

      - name: hgnc_identifier
        in: query
        type: integer
        required: false
        description: 'HGNC identifier'
        default: 620

      - name: limit
        in: query
        type: integer
        required: false
        default: 1
    """
    allowed_str_args = ['hgnc_symbol']

    allowed_int_args = ['mgdid', 'limit', 'hgnc_identifier']

    args = get_args(
        request_args=request.args,
        allowed_int_args=allowed_int_args,
        allowed_str_args=allowed_str_args
    )

    return jsonify(query.mgd(**args))


@app.route("/api/query/uniprot/", methods=['GET', 'POST'])
def uniprot():
    """
    Returns list of Universal Protein Resource (UniProt) protein accessions by query paramaters
    ---

    tags:

      - Query functions

    parameters:

      - name: uniprotid
        in: query
        type: string
        required: false
        description: 'Universal Protein Resource (UniProt) protein accession'
        default: P05067

      - name: hgnc_symbol
        in: query
        type: string
        required: false
        description: 'HGNC symbol'
        default: 'APP'

      - name: hgnc_identifier
        in: query
        type: integer
        required: false
        description: 'HGNC identifier'
        default: 620

      - name: limit
        in: query
        type: integer
        required: false
        default: 1
    """
    allowed_str_args = ['hgnc_symbol', 'uniprotid']

    allowed_int_args = ['limit', 'hgnc_identifier']

    args = get_args(
        request_args=request.args,
        allowed_int_args=allowed_int_args,
        allowed_str_args=allowed_str_args
    )

    return jsonify(query.uniprot(**args))


@app.route("/api/query/ccds/", methods=['GET', 'POST'])
def ccds():
    """
    Returns list of Consensus CDS IDs by query paramaters
    ---

    tags:

      - Query functions

    parameters:

      - name: ccdsid
        in: query
        type: string
        required: false
        description: 'Consensus CDS ID'
        default: 'CCDS13576'

      - name: hgnc_symbol
        in: query
        type: string
        required: false
        description: 'HGNC symbol'
        default: 'APP'

      - name: hgnc_identifier
        in: query
        type: integer
        required: false
        description: 'HGNC identifier'
        default: 620

      - name: limit
        in: query
        type: integer
        required: false
        default: 1
    """
    allowed_str_args = ['hgnc_symbol', 'ccdsid']

    allowed_int_args = ['limit', 'hgnc_identifier']

    args = get_args(
        request_args=request.args,
        allowed_int_args=allowed_int_args,
        allowed_str_args=allowed_str_args
    )

    return jsonify(query.ccds(**args))


@app.route("/api/query/pubmed/", methods=['GET', 'POST'])
def pubmed():
    """
    Returns list of Pubmed and Europe Pubmed Central PMIDs by query paramaters
    ---

    tags:

      - Query functions

    parameters:

      - name: pubmedid
        in: query
        type: integer
        required: false
        description: 'Pubmed and Europe Pubmed Central PMID'
        default: 1679289

      - name: hgnc_symbol
        in: query
        type: string
        required: false
        description: 'HGNC symbol'
        default: 'APP'

      - name: hgnc_identifier
        in: query
        type: integer
        required: false
        description: 'HGNC identifier'
        default: 620

      - name: limit
        in: query
        type: integer
        required: false
        default: 1
    """
    allowed_str_args = ['hgnc_symbol']

    allowed_int_args = ['pubmedid', 'limit', 'hgnc_identifier']

    args = get_args(
        request_args=request.args,
        allowed_int_args=allowed_int_args,
        allowed_str_args=allowed_str_args
    )

    return jsonify(query.pubmed(**args))


@app.route("/api/query/ena/", methods=['GET', 'POST'])
def ena():
    """
    Returns list of European Nucleotide Archive (ENA) identifiers by query paramaters
    ---

    tags:

      - Query functions

    parameters:

      - name: enaid
        in: query
        type: string
        required: false
        description: 'European Nucleotide Archive (ENA) identifier'
        default: 'M15533'

      - name: hgnc_symbol
        in: query
        type: string
        required: false
        description: 'HGNC symbol'
        default: 'APP'

      - name: hgnc_identifier
        in: query
        type: integer
        required: false
        description: 'HGNC identifier'
        default: 620

      - name: limit
        in: query
        type: integer
        required: false
        default: 1
    """
    allowed_str_args = ['hgnc_symbol', 'enaid']

    allowed_int_args = ['limit', 'hgnc_identifier']

    args = get_args(
        request_args=request.args,
        allowed_int_args=allowed_int_args,
        allowed_str_args=allowed_str_args
    )

    return jsonify(query.ena(**args))


@app.route("/api/query/enzyme/", methods=['GET', 'POST'])
def enzyme():
    """
    Returns list of Enzyme Commission numbers by query paramaters
    ---

    tags:

      - Query functions

    parameters:

      - name: ec_number
        in: query
        type: string
        required: false
        description: 'Enzyme Commission number'
        default: '1.1.1.1'

      - name: hgnc_symbol
        in: query
        type: string
        required: false
        description: 'HGNC symbol'
        default: 'ADH7'

      - name: hgnc_identifier
        in: query
        type: integer
        required: false
        description: 'HGNC identifier'
        default: 256

      - name: limit
        in: query
        type: integer
        required: false
        default: 1
    """
    allowed_str_args = ['hgnc_symbol', 'ec_number']

    allowed_int_args = ['limit', 'hgnc_identifier']

    args = get_args(
        request_args=request.args,
        allowed_int_args=allowed_int_args,
        allowed_str_args=allowed_str_args
    )

    return jsonify(query.enzyme(**args))


@app.route("/api/query/lsdb/", methods=['GET', 'POST'])
def lsdb():
    """
    Returns list of Locus Specific Mutation Database entries by query paramaters
    ---

    tags:

      - Query functions

    parameters:

      - name: lsdb
        in: query
        type: string
        required: false
        description: 'Locus Specific Mutation Database ID/name'
        default: 'LRG_795'

      - name: url
        in: query
        type: string
        required: false
        description: 'Locus Specific Mutation Database url'
        default: 'http://www.lrg-sequence.org/LRG/%'

      - name: hgnc_symbol
        in: query
        type: string
        required: false
        description: 'HGNC symbol'
        default: 'A4GALT'

      - name: hgnc_identifier
        in: query
        type: integer
        required: false
        description: 'HGNC identifier'
        default: 18149

      - name: limit
        in: query
        type: integer
        required: false
        default: 1
    """
    allowed_str_args = ['hgnc_symbol', 'lsdb', 'url']

    allowed_int_args = ['limit', 'hgnc_identifier']

    args = get_args(
        request_args=request.args,
        allowed_int_args=allowed_int_args,
        allowed_str_args=allowed_str_args
    )

    return jsonify(query.lsdb(**args))


def get_app():
    app.secret_key = 'sdjfgaksjf326742b45uztcfq'
    return app
