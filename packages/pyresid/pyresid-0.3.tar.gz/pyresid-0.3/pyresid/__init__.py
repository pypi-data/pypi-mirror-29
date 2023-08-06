#!/usr/bin/env python3
"""
`pyresid`

Python tools for mining Protein Residuals from Fulltext articles using PMC number, ePMC and PDB.

author: robert.firth@stfc.ac.uk
"""

import re
import os
import requests
import json
import warnings

import spacy as spacy
import numpy as np
import CifFile as CifFile
import fuzzywuzzy as fw
from collections import OrderedDict
from matplotlib import pyplot as plt
from bs4 import BeautifulSoup
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from Bio.PDB import MMCIFParser
from pandas import DataFrame, read_table
from ftplib import FTP

__author__ = "Rob Firth"
__version__ = "0.3"
__all__ = ["identify_residues",
           "locate_residues",
           "locate_residues2",
           "process",
           "MyEncoder"
           "get_sections_text",
           "reconstruct_fulltext",
           "get_text",
           "aa_dict",
           "short_aa_dict",
           "setup_plot_defaults",
           ]

mmCIF_dir = os.path.abspath(os.path.join(__file__, os.pardir, "mmCIF/"))
PDB_dir = os.path.abspath(os.path.join(__file__, os.pardir, "PDB/"))

EBI_whitelist = ["Title",
                "Abstract",
                "Introduction",
                "Methods",
                "Results",
                "Discussion",
                "Acknowledgments",
                "References",
                "Article",
                "Table",
                "Figure",
                "Case study",
                "Supplementary material",
                "Conclusion",
                "Abbreviations",
                "Competing Interests",
                "Author Contributions"
                ]

aa_dict = {"Ala": {"short_id": "A", "full_id": "Alanine", },
           "Arg": {"short_id": "R", "full_id": "Arginine", },
           "Asn": {"short_id": "N", "full_id": "Asparagine", },
           "Asp": {"short_id": "D", "full_id": "Aspartic acid (Aspartate)", },
           "Cys": {"short_id": "C", "full_id": "Cysteine", },
           "Gln": {"short_id": "Q", "full_id": "Glutamine", },
           "Glu": {"short_id": "E", "full_id": "Glutamic acid (Glutamate)", },
           "Gly": {"short_id": "G", "full_id": "Glycine", },
           "His": {"short_id": "H", "full_id": "Histidine", },
           "Ile": {"short_id": "I", "full_id": "Isoleucine", },
           "Leu": {"short_id": "L", "full_id": "Leucine", },
           "Lys": {"short_id": "K", "full_id": "Lysine", },
           "Met": {"short_id": "M", "full_id": "Methionine", },
           "Phe": {"short_id": "F", "full_id": "Phenylalanine", },
           "Pro": {"short_id": "P", "full_id": "Proline", },
           "Ser": {"short_id": "S", "full_id": "Serine", },
           "Thr": {"short_id": "T", "full_id": "Threonine", },
           "Trp": {"short_id": "W", "full_id": "Tryptophan", },
           "Tyr": {"short_id": "Y", "full_id": "Tyrosine", },
           "Val": {"short_id": "V", "full_id": "Valine", },
           "Asx": {"short_id": "B", "full_id": "Aspartic acid or Asparagine", },
           "Glx": {"short_id": "Z", "full_id": "Glutamine or Glutamic acid.", },
           "Xaa": {"short_id": "X", "full_id": "Any amino acid.", },
           "TERM": {"short_id": None, "full_id": "termination codon", }
           }

short_aa_dict = {"A": {"id": "Ala", "full_id": "Alanine", },
                 "R": {"id": "Arg", "full_id": "Arginine", },
                 "N": {"id": "Asn", "full_id": "Asparagine", },
                 "D": {"id": "Asp", "full_id": "Aspartic acid (Aspartate)", },
                 "C": {"id": "Cys", "full_id": "Cysteine", },
                 "Q": {"id": "Gln", "full_id": "Glutamine", },
                 "E": {"id": "Glu", "full_id": "Glutamic acid (Glutamate)", },
                 "G": {"id": "Gly", "full_id": "Glycine", },
                 "H": {"id": "His", "full_id": "Histidine", },
                 "I": {"id": "Ile", "full_id": "Isoleucine", },
                 "L": {"id": "Leu", "full_id": "Leucine", },
                 "K": {"id": "Lys", "full_id": "Lysine", },
                 "M": {"id": "Met", "full_id": "Methionine", },
                 "F": {"id": "Phe", "full_id": "Phenylalanine", },
                 "P": {"id": "Pro", "full_id": "Proline", },
                 "S": {"id": "Ser", "full_id": "Serine", },
                 "T": {"id": "Thr", "full_id": "Threonine", },
                 "W": {"id": "Trp", "full_id": "Tryptophan", },
                 "Y": {"id": "Tyr", "full_id": "Tyrosine", },
                 "V": {"id": "Val", "full_id": "Valine", },
                 "B": {"id": "Asx", "full_id": "Aspartic acid or Asparagine", },
                 "Z": {"id": "Glx", "full_id": "Glutamine or Glutamic acid.", },
                 "X": {"id": "Xaa", "full_id": "Any amino acid.", },
                 "None": {"id": "TERM", "full_id": "termination codon", }
                 }

extract = lambda x, y: OrderedDict(zip(x, map(y.get, x)))


def setup_plot_defaults():
    """

    Sets up default plot settings for figures.

    Parameters
    ----------


    Returns
    -------

    """

    plt.rcParams['ps.useafm'] = True
    plt.rcParams['pdf.use14corefonts'] = True
    plt.rcParams['text.usetex'] = True
    plt.rcParams['font.size'] = 14
    plt.rcParams['figure.subplot.hspace'] = 0.1
    plt.rc('font', family='sans-serif')
    plt.rc('font', serif='Helvetica')
    pass


class MyEncoder(json.JSONEncoder):
    """

    """

    def default(self, obj):
        if isinstance(obj, OrderedDict):
            return obj
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, spacy.tokens.token.Token):
            return str(obj)
        else:
            return super(MyEncoder, self).default(obj)


def request_fulltextXML(ext_id):
    """
    Requests a fulltext XML document from the ePMC REST API. Raises a warning if this is not
    possible

    Parameters
    ----------
    ext_id : String
         ePMC identifier used to retrieve the relevant entry. Format is prefix of 'PMC'
         followed by an integer.

    Returns
    -------
    r : `Requests.Response <http://docs.python-requests.org/en/master/api/#requests.Response>`_
        The response to the query served up by the requests package.
    """
    request_url = "https://www.ebi.ac.uk/europepmc/webservices/rest/" + ext_id + "/fullTextXML"

    r = requests.get(request_url)

    if r.status_code == 200:
        return r
    else:
        warnings.warn("request to " + str(ext_id) + " has failed to return 200, and has returned " + str(r.status_code))
    pass


def parse_request(ext_id):
    """
    Wrapper for :func:`~pyresid.request_fulltextXML` that returns a `BeautifulSoup` XML object

    Parameters
    ----------
    ext_id : String
         ePMC identifier used to retrieve the relevant entry. Format is prefix of 'PMC'
         followed by an integer.

    Returns
    -------

    soup : `BeautifulSoup <https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.html#beautifulsoup>`_
        BeautifulSoup XML object created from the text response from  :func:`pyresid.request_fulltextXML`


    See Also
    --------
    :func:`~pyresid.request_fulltextXML`

    """
    r = request_fulltextXML(ext_id=ext_id)
    soup = BeautifulSoup(r.text, "lxml-xml")

    return soup


def get_metadata(ext_id):
    """
    Query EBI ePMC API, extract "article-meta"

    Parameters
    ----------
    ext_id : String
         ePMC identifier used to retrieve the relevant entry. Format is prefix of 'PMC'
         followed by an integer.

    Returns
    -------
    meta_dict : Dict
            Dictionary containing metadata, including the title and authors
    """
    soup = parse_request(ext_id=ext_id)

    meta = soup.findAll("article-meta")

    meta_dict = {}
    meta_dict["title"] = meta[0].find(re.compile("^title")).text
    meta_dict["authors"] = []

    for author in meta[0].findAll("contrib"):
        auth_dict = {}

        auth_dict["given_name"] = author.find("given-names").text
        auth_dict["surname"] = author.find("surname").text
        meta_dict["authors"].append(auth_dict)

    return (meta_dict)


def get_all_text(ext_id):
    """
    Wrapper for `~pyresid.parse_request`

    Parameters
    ----------
    ext_id : String
         ePMC identifier used to retrieve the relevant entry. Format is prefix of 'PMC'
         followed by an integer.

    Returns
    -------
    soup : `BeautifulSoup <https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.html#beautifulsoup>`_
        BeautifulSoup XML object created from the text response from  :func:`pyresid.request_fulltextXML`

    """

    return parse_request(ext_id=ext_id).get_text(" ")


def get_sections_text(ext_id, remove_tables=True, fulltext=False, verbose=False):
    """
    Requests fulltext XML from the EBI ePMC web REST API, parses the response into a dict.

    Parameters
    ----------
    ext_id : String
         ePMC identifier used to retrieve the relevant entry. Format is prefix of 'PMC'
         followed by an integer.

    remove_tables : Bool, optional, default: True
                Flag to ignore the text found within tables.

    fulltext : Bool, optional, default: False
           Flag used to return a 'dumb' fulltext (rather than that
           from :func:`~pyresid.reconstruct_fulltext`)

    verbose : Bool, optional, default: False
          Flag to turn on verbose output

    Returns
    -------
    text_dict : OrderedDict
            Dictionary containing the parsed XML. Each entry corresponds to a Section
            in the XML (technically a child of the `<body>`).

    See Also
    --------
    * :func:`~pyresid.request_fulltextXML`
    * :func:`~pyresid.parse_request`
    * :func:`~pyresid.reconstruct_fulltext`

    """

    soup = parse_request(ext_id=ext_id)

    if remove_tables:
        for i in range(0, len(soup('table'))):  # https://stackoverflow.com/q/18934136
            soup.table.decompose()

    if fulltext:
        return " ".join([sec.get_text(" ") for sec in soup.findAll("sec")])
    else:
        text_dict = OrderedDict()

    for sec_number, sec in enumerate(soup.find("body").children):

        title = sec.find("title")

        if "id" in sec.attrs:
            if verbose: print("hasid")
            sec_id = sec["id"]
        if title:
            if verbose: print("hastitle")
            sec_id = title.text.strip()

        if "id" not in sec.attrs and not title:
            warnings.warn("cannot id the section")
            sec_id = str(sec_number)

        if verbose: print(sec_id, end="")

        if title:
            title = title.text.strip()
        else:
            title = sec_id
        if sec_id not in text_dict:
            text_dict[sec_id] = {"title": title, "text": sec.get_text(" ")}
        else:
            i = 1
            while sec_id not in text_dict:
                sec_id = sec_id + str(i)
                text_dict[sec_id] = {"title": title, "text": sec.get_text(" ")}
                i += 1
        if verbose: print("")

    return text_dict


def _deprecated_get_sections_text(ext_id, remove_tables=True, fulltext=False):
    """
    DEPRECATED

    Parameters
    ----------
    ext_id : String
         ePMC identifier used to retrieve the relevant entry. Format is prefix of 'PMC'
         followed by an integer.

    remove_tables : Bool, optional, default: True
                Flag to ignore the text found within tables.

    fulltext : Bool, optional, default: False
           Flag used to return a 'dumb' fulltext (rather than that
           from :func:`~pyresid.reconstruct_fulltext`)

    Returns
    -------
    text_dict : OrderedDict
            Dictionary containing the parsed XML. Each entry corresponds to a Section
            in the XML (technically a child of the `<body>`).
    """
    soup = parse_request(ext_id=ext_id)

    if remove_tables:
        for i in range(0, len(soup('table'))):  # https://stackoverflow.com/q/18934136
            soup.table.decompose()

    if fulltext:
        return " ".join([sec.get_text(" ") for sec in soup.findAll("sec")])
    else:
        text_dict = OrderedDict()
        for sec in soup.findAll("sec"):
            if not sec.find_parent("sec"):  # https://stackoverflow.com/a/31208775
                try:
                    sec_id = sec["id"]
                    title = sec.find("title")

                    if title:
                        title = title.text

                    text_dict[sec_id] = {"title": title, "text": sec.get_text(" ")}

                except:
                    pass

        return text_dict


def get_text(ext_id, verbose=False):
    """
    A wrapper for :func:`~pyresid.get_sections_text` that adds additional information
    to the *text_dict*.

    Parameters
    ----------
    ext_id : String
         ePMC identifier used to retrieve the relevant entry. Format is prefix of 'PMC'
         followed by an integer.

    verbose : Bool, optional, default: False
          Flag to turn on verbose output

    Returns
    -------

    text_dict : OrderedDict
            Dictionary containing the parsed XML. Each entry corresponds to a Section
            in the XML (technically a child of the `<body>`). An augmented version of
            the *text_dict* returned by :func:`~pyresid.get_sections_text` - containing
            additional information including spaCy tokens, length in characters and
            starting offset.

    See Also
    --------
    * :func:`~pyresid.get_sections_text`
    """

    text_dict = get_sections_text(ext_id=ext_id, remove_tables=True, fulltext=False)

    nlp = spacy.load('en')

    for i, sec in enumerate(text_dict):
        if verbose:
            print("This sec=", sec)

        doc = nlp(text_dict[sec]["text"])
        text_dict[sec]["tokens"] = [t for t in doc]
        text_dict[sec]["len"] = len(
            text_dict[sec]["tokens"])  ## this len is number of tokens. Also want number of chars
        text_dict[sec]["char_len"] = len(text_dict[sec]["text"])
        if verbose:
            print("char_len is ", text_dict[sec]["char_len"])
        if i == 0:
            text_dict[sec]["start"] = 0
            text_dict[sec]["offset"] = 0
        else:
            text_dict[sec]["start"] = text_dict[list(text_dict.keys())[i - 1]]["start"] + \
                                      text_dict[list(text_dict.keys())[i - 1]]["len"]
            text_dict[sec]["offset"] = text_dict[list(text_dict.keys())[i - 1]]["offset"] + \
                                       text_dict[list(text_dict.keys())[i - 1]]["char_len"]

            if verbose:
                print("Previous sec = ", list(text_dict.keys())[i - 1])
                print("Previous sec char_len = ", text_dict[list(text_dict.keys())[i - 1]]["char_len"])

    return text_dict


def query_ID_converter(ext_id):
    """
    Converts ePMC ext_id into PMID , API description here - https://www.ncbi.nlm.nih.gov/pmc/tools/id-converter-api/

    Parameters
    ----------
    ext_id : String
         ePMC identifier used to retrieve the relevant entry. Format is prefix of 'PMC'
         followed by an integer.

    Returns
    -------
    response_json : dict
                json returned by the API containing the relevant information. Can be passed to
                :func:`~pyre.convert_PMCID_to_PMID`

    See Also
    --------
    * :func:`~pyre.convert_PMCID_to_PMID`
    """

    service_root_url = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids="

    request_url = service_root_url + ext_id

    fmt = "json"
    request_url = request_url + r"&format=" + fmt

    tool = "pyresid"
    request_url = request_url + r"&tool=" + tool

    email = "robert.firth@stfc.ac.uk"
    request_url = request_url + r"&email=" + email

    r = requests.get(request_url)
    response_json = json.loads(r.text)

    return response_json


def convert_PMCID_to_PMID(ext_id):
    """
    Converts ePMC ID into PubMed ID

    Parameters
    ----------
    ext_id : String
         ePMC identifier used to retrieve the relevant entry. Format is prefix of 'PMC'
         followed by an integer.

    Returns
    -------
    pmid : string
       PubMed URI corresponding to the PMC ID URI supplied

    """
    data_obj = query_ID_converter(ext_id=ext_id)
    pmid = data_obj["records"][0]["pmid"]
    return pmid


def reconstruct_fulltext(text_dict, tokenise=True, verbose=False):
    """
    Converts a *text_dict* into a single string or series of tokens in a list of strings.

    Parameters
    ----------
    text_dict : Dict or OrderedDict
            Dictionary containing the parsed XML. Each entry corresponds to a Section
            in the XML. Usually an output from :func:`~pyresid.get_sections_text`

    tokenise : Bool, optional, default: False
           Flag to enable or disable the reconstructed text being returned as spaCy tokens
           rather than a string

    verbose : Bool, optional, default: False
          Flag to turn on verbose output


    Returns
    -------

    fulltext : string
           text snippet to be searched for residues.

    OR

    fulltext_tokens : List of strings
                  Array of tokens that can be used, for example, to search for
                  *residue_mentions*.

    See Also
    --------
    :func:`~pyresid.get_sections_text`

    """

    fulltext = " ".join([text_dict[sec]["text"] for sec in text_dict])

    if tokenise:
        if verbose:
            print("Tokenising...")
        nlp = spacy.load('en')
        fulldoc = nlp(fulltext)
        fulltext_tokens = [t.text for t in fulldoc]

        return fulltext_tokens
    else:
        return fulltext


def identify_residues(fulltext, return_mentions=False, short=False, verbose=False):
    """
    Identify the residues that are mentioned within a string of text.

    Parameters
    ----------
    fulltext :  string
                text snippet to be searched for residues.

    return_mentions : Bool, optional, default: False
                      Flag passed to determine whether to return the residue that matches, or the specific
                      mention that triggers the identification. e.g. for the string "Arg123/125", with
                      *return_mentions* =False would return {"Arg123", "Arg125"}, while *return_mentions* =True
                      would return {"Arg123/125"}.

    short : Bool, optional, default: False
            Enable the matching of "short" Amino-Acid codes, such as "A123", as well as the three-letter
            default nomenclature.

    verbose : Bool, optional, default: False
              Flag to turn on verbose output

    Returns
    -------

    unique_mentions : Set
                      Matches found within *fulltext*

    See Also
    --------
    * `pyresid.aa_dict` : Dictionary with three letter Amino-Acid identifiers as keys, and items that allow translation to short identifiers or full names.
    * `pyresid.short_aa_dict` : Dictionary with short Amino-Acid identifiers as keys, and items that allow translation to three letter codes or full names.

    """

    prefixes = list(aa_dict.keys())

    pattern = "[a-zA-Z]{3}\d+/\d+|[a-zA-Z]{3}\d+"

    p = re.compile(pattern)

    unique_mentions = set([i.strip() for i in p.findall(fulltext) if "".join(filter(str.isalpha, i)) in prefixes])

    if short:
        short_prefixes = list(short_aa_dict.keys())
        pattern = r"\b[a-zA-Z]\d+\b"
        p = re.compile(pattern)
        unique_short_mentions = set(
            [i.strip() for i in p.findall(fulltext) if "".join(filter(str.isalpha, i)) in short_prefixes])

        unique_mentions.update(unique_short_mentions)

    if return_mentions:
        return unique_mentions

    unique_residues = []
    for i in unique_mentions:
        if verbose:
            print(i)
        if "/" in i:
            residue_position = ["".join(filter(str.isdigit, j)) for j in i.split("/")]
            aa_residue_id = [j for j in ["".join(filter(str.isalpha, i)) for i in i.split("/")] if j]
            decomposed = [x + y for x in aa_residue_id for y in
                          residue_position]  ## TODO - https://stackoverflow.com/a/19560204
            unique_residues += decomposed
        else:
            unique_residues.append(i)

    return set(unique_residues)


def check_residue_candidate_validity(cand, pattern="[a-zA-Z]{3}\d+/\d+|[a-zA-Z]{3}\d+", verbose=False):
    """

    Parameters
    ----------
    cand : String
       Candidate residue to check for validity

    pattern : String, optional, default : "[a-zA-Z]{3}\d+/\d+|[a-zA-Z]{3}\d+".
          Regular Expression with which to match the candidate.

    verbose : Bool, optional, default: False
          Flag to turn on verbose output

    Returns
    -------
    match_bool_list : List of Bool.
                  List of True/False booleans reflecting the validity of the input candidates.

    """
    if type(cand) in {np.str, str} or not hasattr(cand, "__iter__"):
        if verbose:
            print(cand)
        match = re.match(pattern, cand.strip())

        if match:
            if verbose:
                print("Format Match")

            isolated_aa = "".join(filter(str.isalpha, cand)).strip()

            if verbose:
                print("isolatedAA = ", isolated_aa)

            if isolated_aa.lower() in [i.lower() for i in aa_dict.keys()]:
                if verbose:
                    print("OK")

                return True

            else:
                if verbose:
                    print("Not OK")
                return False

        else:
            if verbose:
                print("Not OK, format mismatch")

            return False
    else:
        match_bool_list = []
        for candidate in cand:
            if verbose:
                print(candidate)
            match_bool_list.append(check_residue_candidate_validity(candidate))
        return match_bool_list


def decompose_slashed_residue(i):
    """

    Parameters
    ----------
    i :

    Returns
    -------

    """
    # if "/" in i:
    #     residue_position = ["".join(filter(str.isdigit, j)) for j in i.split("/")]
    #     aa_residue_id = [j for j in ["".join(filter(str.isalpha, i)) for i in i.split("/")] if j]
    #     decomposed = [x + y for x in aa_residue_id for y in residue_position] ## TODO doesn't do what I think
    #     return decomposed
    # else:
    #     return [i,]
    return list(identify_residues(i))


def subdivide_compound_residues(instring, verbose=False):
    """

    Parameters
    ----------
    instring : String
           Input compound candidate to decompose into a number of actual residue ids.

    verbose : Bool, optional, default: False
          Flag to turn on verbose output

    Returns
    -------

    """

    if verbose: print(instring)
    cands = instring.split("/")
    validity = check_residue_candidate_validity(cands)
    sublists = []
    x = []  ## Need this in case element 1 is not valid?

    for i, boolean_value in enumerate(validity):
        if verbose: print(i, boolean_value)
        if boolean_value:

            if i > 0:
                sublists.extend(decompose_slashed_residue("/".join(x)))

            x = [cands[i], ]

        else:

            x.append(cands[i])

    sublists.extend(decompose_slashed_residue("/".join(x)))
    return (sublists)


def identify_protein_ID(fulltext, simple=False, infile=None, locdir=None, verbose=False):
    """


    Parameters
    ----------
    fulltext :  string
            text snippet to be searched for residues.

    simple : Bool, optional, default: False
         Flag that, if set, will skip the check against the PDB. Generally a bad idea.

    infile : String or Path, optional, None
         File to load in order to check candidate PDB entries against. contains the PDB entries -
         if `None` defaults to "PDBID.list"

    locdir : String or Path, optional, default: None
         Directory that contains the infile. If None, default is assumed to be `PDB_dir`, if this
         is not found then will be the user home.

    verbose : Bool, optional, default: False
              Flag to turn on verbose output

    Returns
    -------
    unique_protiens : Set
                  Matches found within `fulltext`
    See Also
    --------
    :func:`~pyresid.identify_residues`
    :func:`~pyresid.load_protein_IDs`
    """

    ## TODO - Case insensitive - missed all pdb entries in PMC5297931

    # pattern = r"\b[0-9][A-Z0-9]{3}\b"
    pattern = r"\b[0-9][a-zA-Z0-9]{3}\b"

    p = re.compile(pattern)

    pdb_id_candidates = p.findall(fulltext)

    if verbose:
        print(pdb_id_candidates)

    unique_mentions = set(pdb_id_candidates)

    if simple:
        return list(unique_mentions)

    unique_protiens = []
    pdb_ids = load_protein_IDs(infile=infile, locdir=locdir)

    if verbose:
        print("Checking against PDB.")

    for candidate in unique_mentions:
        if candidate.upper() in pdb_ids:
            if verbose:
                print(candidate)

            unique_protiens.append(candidate)

    return unique_protiens


def locate_proteins(fulltext_tokens, text_dict, unique_proteins, verbose=False):
    """

    Parameters
    ----------
    fulltext_tokens : List of strings
                  Array of tokens to search for `residue_mentions`, typically
                  the output from :func:`~pyresid.reconstruct_fulltext`.

    text_dict : Dict or OrderedDict
            Dictionary containing the parsed XML. Each entry corresponds to a Section
            in the XML. Usually an output from :func:`~pyresid.get_sections_text`

    unique_proteins : Set, or other iterable.
                   Typically output from :func:`~pyresid.identify_protein_ID`,
                   the protein structures which to locate within `fulltext_tokens`.

    verbose : Bool, optional, default: False
          Flag to turn on verbose output

    Returns
    -------
    location_dict : OrderedDict
                Ordered dictionary containing the locations, matched string
                and frequency of each of the protein structure mentions passed, which
                are themselves used as the dict keys.
    See Also
    --------
    * :func:`~pyresid.locate_residues`
    * :func:`~pyresid.identify_protein_ID`
    """

    sec_names = [text_dict[i]["title"] for i in text_dict]
    sec_offset = [text_dict[i]["offset"] for i in text_dict]

    location_dict = OrderedDict()

    for tkn in unique_proteins:

        if tkn not in location_dict:
            location_dict[tkn] = OrderedDict()

            location_dict[tkn]["offset"] = []
            location_dict[tkn]["locations"] = []
            location_dict[tkn]["string"] = []
            location_dict[tkn]["freq"] = 0

        if verbose:
            print(tkn)

        locations = [word for word in enumerate(fulltext_tokens) if
                     tkn in str(word[1])]
        offsets = [word[1].idx for word in locations]
        if verbose:
            print(locations)

        location_dict[tkn]["offset"] += [word[1].idx for word in locations]
        location_dict[tkn]["locations"] += list(np.array(locations).T[0].astype(int))
        location_dict[tkn]["string"] += list(np.array(locations).T[1])

        location_dict[tkn]["freq"] += len(locations)

    return location_dict


def load_protein_IDs(infile=None, locdir=None):
    """
    Reads in list of valid (approved and pending) PDB entries.

    Parameters
    ----------
    infile : String or Path, optional, default: None
         File that contains the PDB entries - defaults to "PDBID.list"

    locdir : String or Path, optional, default: None
         Directory that contains the infile. If None, default is assumed to be `PDB_dir`, if this
         is not found then will be the user home.

    Returns
    -------
    pdb_arr : List of strings
        List of valid (approved and pending) PDB entries

    See Also
    --------
    * :func:`pyresid.combine_compound_IDs`
    * :func:`pyresid.get_compound_IDfiles`

    """
    if not locdir:
        if os.path.exists(PDB_dir):
            locdir = PDB_dir
        if "HOME" in os.environ:
            locdir = os.environ["HOME"]
        elif "HOMEPATH" in os.environ:
            locdir = os.environ["HOMEPATH"]
    if not infile:
        infile = os.path.join(locdir, "PDBID.list")

    pdb_arr = list(np.loadtxt(infile, dtype=str))

    return pdb_arr


def combine_compound_IDs(source_infile=None, pending_infile=None, outfile=None, locdir=None, outdir=None,
                         save=True, return_df=False):
    """

    Parameters
    ----------
    source_infile :

    pending_infile :

    outfile :

    locdir :

    outdir :

    save :

    return_df :


    Returns
    -------

    """

    if not locdir:
        if "HOME" in os.environ:
            locdir = os.environ["HOME"]
        elif "HOMEPATH" in os.environ:
            locdir = os.environ["HOMEPATH"]

    if not source_infile:
        source_infile = os.path.join(locdir, "FTP_source.idx")
    if not pending_infile:
        pending_infile = os.path.join(locdir, "FTP_pending.list")

    current_prot_df = read_table(source_infile, skiprows=4, header=None, names=["PDBID", "name"])

    idcodes = []
    description = []
    next_line_is_description_better_set_a_flag = False

    with open(pending_infile, "r") as infile:
        for line in infile:
            try:
                if next_line_is_description_better_set_a_flag:
                    description.append(line)
                    next_line_is_description_better_set_a_flag = False

                if line.split()[0] == "Idcode:":
                    #                 print(line)
                    idcodes.append(line.split()[1])
                if line.split()[0] == "Entry":
                    next_line_is_description_better_set_a_flag = True

            except:
                pass

    pending_prot_df = DataFrame(list(zip(idcodes, description)), columns=["PDBID", "name"])

    prot_df = current_prot_df.append(pending_prot_df)

    if save:
        if not outdir:
            if "HOME" in os.environ:
                outdir = os.environ["HOME"]
            elif "HOMEPATH" in os.environ:
                outdir = os.environ["HOMEPATH"]
        if not outfile:
            outfile = os.path.join(outdir, "PDBID.list")

        prot_df["PDBID"].to_csv(outfile, index=False)

    if return_df:
        return prot_df
    else:
        pass


def get_compound_IDfiles(ftp_url="ftp.wwpdb.org", outdir=None, pending=True):
    """

    Parameters
    ----------
    ftp_url :

    outdir :

    pending :


    Returns
    -------

    """

    ftp = FTP(ftp_url)  # connect to host, default port
    ftp.login()  # user anonymous, passwd anonymous@
    ftp.cwd("/pub/pdb/derived_data/index")

    if not outdir:
        if "HOME" in os.environ:
            outdir = os.environ["HOME"]
        elif "HOMEPATH" in os.environ:
            outdir = os.environ["HOMEPATH"]

    source_outfile = os.path.join(outdir, "FTP_source.idx")
    ftp.retrbinary("RETR source.idx", open(source_outfile, "wb").write)

    if pending:
        pending_outfile = os.path.join(outdir, "FTP_pending.list")
        ftp.retrbinary("RETR pending_waiting.list", open(pending_outfile, "wb").write)

    ftp.quit()

    pass


def preprocess_mentions(mentions, verbose=False):
    """

    Parameters
    ----------
    mentions :

    verbose : Bool, optional, default: False
          Flag to turn on verbose output

    Returns
    -------

    """
    unpacked = []

    for i in list(mentions):
        # decomposed = decompose_slashed_residue(i)
        decomposed = subdivide_compound_residues(i)
        if verbose:
            print(decomposed)

        for j in decomposed:
            if j not in unpacked:
                unpacked.append(j)
            else:
                mentions.remove(j)

    return mentions


def locate_residues(fulltext_tokens, residue_mentions, offset=False, verbose=False):
    """
    Locate the already identified residues within tokenised fulltext.

    Parameters
    ----------
    fulltext_tokens : List of strings
                  Array of tokens to search for *residue_mentions*, typically
                  the output from :func:`~pyresid.reconstruct_fulltext`.

    residue_mentions : Set, or other iterable.
                   Typically output from :func:`~pyresid.identify_residues`,
                   the residues which to locate within *fulltext_tokens*.

    offset : Bool, optional, default: False
         Flag to include the location index (idx) within the *location_dict*,
         value is the number of characters the start of the matched string is
         from the start of the fulltext document from which *fulltext_tokens*
         was tokenised.

    verbose : Bool, optional, default: False
          Flag to turn on verbose output

    Returns
    -------

    location_dict : OrderedDict
                Ordered dictionary containing the locations, matched string
                and frequency of each of the residue mentions passed, which
                are themselves used as the dict keys.

    See Also
    --------
    :func:`~pyresid.identify_residues`

    """

    ## preprocess mentions
    residue_mentions = preprocess_mentions(residue_mentions)

    if verbose:
        print(residue_mentions)

    location_dict = OrderedDict()

    for i, tkn in enumerate(residue_mentions):

        # locations = [word for word in enumerate(fulltext_tokens) if tkn in word[1]]
        locations = [word for word in enumerate(fulltext_tokens) if
                     tkn in str(word[1])]  ## Should make it possible to pass spacy tokens
        if verbose:
            print(i, " tkn=", tkn)
            print(locations, len(locations))

        # decomposed = decompose_slashed_residue(tkn)
        decomposed = subdivide_compound_residues(tkn)

        for newtkn in decomposed:

            where = [newtkn in identify_residues(str(word[1]), verbose=False) for word in enumerate(fulltext_tokens)]

            if verbose:
                print("newtkn=", newtkn)
                print("locations = ", np.arange(len(fulltext_tokens))[where])
                print("Strings = ", np.array(fulltext_tokens)[where])

            if newtkn not in location_dict:
                #                 print("unknown")
                location_dict[newtkn] = OrderedDict()
                if offset:
                    location_dict[newtkn]["offset"] = []
                location_dict[newtkn]["locations"] = []
                location_dict[newtkn]["string"] = []
                location_dict[newtkn]["freq"] = 0
            else:
                #                 print("known")
                pass

            location_dict[newtkn]["locations"] = np.arange(len(fulltext_tokens))[where]
            location_dict[newtkn]["string"] = np.array(fulltext_tokens)[where]
            location_dict[newtkn]["freq"] = len(location_dict[newtkn]["locations"])

            if offset:
                location_dict[newtkn]["offset"] = [word.idx for word in location_dict[newtkn]["string"]]

    return location_dict


def _deprecated_locate_residues(fulltext_tokens, unique_residues, fulldoc=None, offset=False, verbose=False):
    """
    DEPRECATED

    Parameters
    ----------
    fulltext_tokens :

    unique_residues :

    fulldoc :

    offset :

    verbose : Bool, optional, default: False
          Flag to turn on verbose output

    Returns
    -------

    """
    location_dict = OrderedDict()

    for tkn in unique_residues:
        if verbose:
            print(tkn)
        # decomposed = decompose_slashed_residue(tkn)
        decomposed = subdivide_compound_residues(tkn)

        for newtkn in decomposed:
            if newtkn not in location_dict:
                location_dict[newtkn] = OrderedDict()
                if offset:
                    location_dict[newtkn]["offset"] = []
                location_dict[newtkn]["locations"] = []
                location_dict[newtkn]["string"] = []
                location_dict[newtkn]["freq"] = 0

            if verbose:
                print(newtkn)

            # locations = [word for word in enumerate(fulltext_tokens) if tkn in word[1]]
            locations = [word for word in enumerate(fulltext_tokens) if
                         tkn in str(word[1])]  ## Should make it possible to pass spacy tokens
            if offset:
                location_dict[newtkn]["offset"] += [word[1].idx for word in locations]

            location_dict[newtkn]["locations"] += list(np.array(locations).T[0].astype(int))
            location_dict[newtkn]["string"] += list(np.array(locations).T[1])
            location_dict[newtkn]["freq"] += len(location_dict[newtkn]["locations"])

            if verbose:
                print(locations)

    return location_dict


def plot_locations(location_dict, text_dict, fulltext_tokens, n=None, title=None, ylabel=None):
    """

    Parameters
    ----------
    location_dict :

    text_dict :

    fulltext_tokens :

    n :

    title :

    ylabel :


    Returns
    -------

    """

    keys_freqency_sorted = np.array(list(location_dict.keys()))[
                               np.argsort([location_dict[res]["freq"] for res in location_dict])][::-1]

    if n:
        if n > len(keys_freqency_sorted):
            n = len(keys_freqency_sorted)
        plot_dict = extract(keys_freqency_sorted[:n], location_dict)
        keys_freqency_sorted = keys_freqency_sorted[:n]
    else:
        plot_dict = location_dict

    fig = plt.figure(figsize=[8, len(plot_dict.keys()) * 0.5])
    fig.subplots_adjust(left=0.15, bottom=0.08, top=0.99,
                        right=0.99, hspace=0, wspace=0)

    ax1 = fig.add_subplot(111)

    for i, key in enumerate(keys_freqency_sorted[::-1]):  # Frequency sorted
        ax1.scatter(plot_dict[key]["locations"], np.ones(len(plot_dict[key]["locations"])) * i, marker="|")

    orig_ylim = ax1.get_ylim()

    for sec in text_dict:
        ax1.plot([text_dict[sec]["start"], text_dict[sec]["start"], ],
                 [np.nanmin(orig_ylim) - 2, np.nanmax(orig_ylim) + 2])  # Introduction
        ax1.text(text_dict[sec]["start"], orig_ylim[1] - 1, text_dict[sec]["title"], rotation="vertical", ha="left")

    plt.yticks(np.arange(len(plot_dict)), keys_freqency_sorted[::-1])

    if n:
        ax1.set_ylim([-0.5, n - 0.5])
    else:
        ax1.set_ylim(orig_ylim)

    if title:
        ax1.set_title(title)

    ax1.set_xlim(-100, len(fulltext_tokens))
    plt.xlabel("Token Number")

    if ylabel:
        plt.ylabel(ylabel)
    else:
        plt.ylabel("Amino Acid")

    pass


def find_clusters(residue_shortid, locations_dict):
    """

    Parameters
    ----------
    residue_shortid
    locations_dict

    Returns
    -------

    """
    X = np.array([locations_dict[residue_shortid]["locations"],
                  list(np.array(
                      locations_dict[residue_shortid]["locations"]) * 0 + 1)]).T  # Assume all are at the same y

    # generate the linkage matrix
    # Z = linkage(X, 'ward')
    # Z = linkage(X, 'single', metric="cosine")
    # Z = linkage(X, 'complete', metric="cosine")
    Z = linkage(X, 'average', metric="cosine")

    return Z


def plot_dendrogram(Z, figsize=[10, 10], orientation="left", leaf_rotation=90., max_d=None,
                    title='Hierarchical Clustering Dendrogram'):
    """

    Parameters
    ----------
    Z :

    figsize :

    orientation :

    leaf_rotation :

    max_d :

    title :


    Returns
    -------

    """
    fig = plt.figure(figsize=figsize)
    fig.subplots_adjust(left=0.15, bottom=0.08, top=0.99,
                        right=0.99, hspace=0, wspace=0)

    ax1 = fig.add_subplot(111)

    # ax1.set_title(r'$\textnormal{Hierarchical Clustering Dendrogram}$')
    # ax1.set_xlabel(r'$\textnormal{sample index}$')
    # ax1.set_ylabel(r'$\textnormal{distance}$')

    if title:
        ax1.set_title(title)
    if orientation == "left" or orientation == "right":
        ax1.set_ylabel('sample index')
        ax1.set_xlabel('distance')
        if orientation == "left":
            ax1.yaxis.set_label_position("right")
    else:
        ax1.set_xlabel('sample index')
        ax1.set_ylabel('distance')

    dendrogram(
        Z,
        orientation=orientation,
        leaf_rotation=leaf_rotation,  # rotates the x axis labels
        leaf_font_size=8.,  # font size for the x axis labels
        ax=ax1
    )

    if max_d:
        plt.axhline(y=max_d, c='k')

    plt.show()
    pass


def plot_disthist(Z, bins=None, max_d=None):
    """

    Parameters
    ----------
    Z :

    bins :

    max_d :


    Returns
    -------

    """
    if not bins:
        binsize = np.nanmax(Z.T[2]) / 20.
        bins = np.linspace(0, np.nanmax(Z.T[2]) + binsize, 100)

    fig = plt.figure(figsize=[8, 4])
    fig.subplots_adjust(left=0.15, bottom=0.08, top=0.99,
                        right=0.99, hspace=0, wspace=0)

    ax1 = fig.add_subplot(111)

    #     hist = ax1.hist(Z.T[2], bins=bins, cumulative=True)
    hist = ax1.hist(Z.T[2], bins=bins)

    if max_d:
        plt.axvline(x=max_d, c="k")

    ax1.set_title("Cluster Distance Histogram")
    ax1.set_xlabel("Distance")
    ax1.set_ylabel("Frequency")
    pass


def plot_clusters(X, Z, max_d, text_dict, fulltext_tokens, residue_shortid):
    """

    Parameters
    ----------
    X :

    Z :

    max_d :

    text_dict :

    fulltext_tokens :

    residue_shortid :


    Returns
    -------

    """

    clusters = fcluster(Z, max_d, criterion='distance')

    fig = plt.figure(figsize=[8, 1])
    fig.subplots_adjust(left=0.15, bottom=0.08, top=0.99,
                        right=0.99, hspace=0, wspace=0)

    ax1 = fig.add_subplot(111)

    ax1.scatter(X[:, 0], X[:, 1], c=clusters, cmap='plasma', marker="|", s=100)

    orig_ylim = ax1.get_ylim()

    ax1.plot([text_dict["Sec1"]["start"], text_dict["Sec1"]["start"], ],
             [np.nanmin(orig_ylim) - 2, np.nanmax(orig_ylim) + 2])  # Introduction
    ax1.text(text_dict["Sec1"]["start"], orig_ylim[1], "Introduction", rotation="vertical", ha="left")
    ax1.plot([text_dict["Sec2"]["start"], text_dict["Sec2"]["start"], ],
             [np.nanmin(orig_ylim) - 2, np.nanmax(orig_ylim) + 2])  # Results
    ax1.text(text_dict["Sec2"]["start"], orig_ylim[1], "Results", rotation="vertical", ha="left")
    ax1.plot([text_dict["Sec12"]["start"], text_dict["Sec12"]["start"], ],
             [np.nanmin(orig_ylim) - 2, np.nanmax(orig_ylim) + 2])  # Discussion
    ax1.text(text_dict["Sec12"]["start"], orig_ylim[1], "Discussion", rotation="vertical", ha="left")

    plt.yticks([1, ], [residue_shortid], )

    ax1.set_ylim(orig_ylim)

    ax1.set_xlim(-100, len(fulltext_tokens))
    plt.xlabel("Token Number")
    plt.ylabel("Amino Acid")
    pass


def query_epmc(query):
    """

    Parameters
    ----------
    query :

    Returns
    -------

    """
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query="
    page_term = "&pageSize=999"  ## Usual limit is 25
    request_url = url + query + page_term
    r = requests.get(request_url)

    if r.status_code == 200:
        return r
    else:
        warnings.warn("request to " + str(query) + " has failed to return 200, and has returned " + str(r.status_code))
    pass


def query_to_dict(query):
    """

    Parameters
    ----------
    query :

    Returns
    -------

    """
    r = query_epmc(query)
    soup = BeautifulSoup(r.text, "lxml-xml")

    results_dict = OrderedDict()

    for result in soup.resultList:
        #     print(result.title)
        results_dict[result.id] = {}

        for i in result:
            results_dict[result.id][i.name] = i.text

    return results_dict


def extract_ids_from_query(query):
    """

    Parameters
    ----------
    query :

    Returns
    -------

    """

    results_dict = query_to_dict(query)

    ids = [results_dict[i]["pmcid"] for i in results_dict]

    return ids


def get_rawcontext(location_dict, fulltext, x=50, verbose=False):
    """

    Parameters
    ----------
    location_dict : OrderedDict
                Ordered dictionary containing the locations, matched string
                and frequency of each of the residue mentions passed, which
                are themselves used as the dict keys.

    fulltext :  string
                text snippet to be subdivide for context.

    x : int, optional, default: 50
        How much context to include

    verbose : Bool, optional, default: False
          Flag to turn on verbose output

    Returns
    -------
    location_dict : OrderedDict
                Returns an augmented version of the input `location_dict`, with the context
                added as an item under the key "rawcontext" for each unique mention and location
    """
    for key in location_dict:
        if verbose:
            print(key)
        for i, offset in enumerate(location_dict[key]["offset"]):
            if i == 0:
                location_dict[key]["rawcontext"] = []

            #             rawcontext = "".join(fulltext[offset-x:offset+x])
            rawcontext = [fulltext[offset - x:offset + x], ]

            location_dict[key]["rawcontext"] += rawcontext

            if verbose:
                print(rawcontext)
    return location_dict


def process(ext_id_list, outdir, filename="pyresid_output.json", save=True, return_dict=False, cifscantype='flex',
            context="sent", use_actual_sections=False, verbose=False):
    """
    This wraps the main workhorse functions, taking a list of PMC IDs and mining the resulting fulltext.
    output is a json structure (the encoded output of locate_residues2 saved with MyEncoder), to match
    the EBI specifications.

    Parameters
    ----------
    ext_id_list : List of strings
         List containing ePMC identifiers used to retrieve the relevant entry. Format is prefix of 'PMC'
         followed by an integer.

    outdir : String or Path
         Directory that will contain the output file.

    filename : String
         The structured output JSON file containing the annotations, one line per `ext_id`.

    save : Bool, optional, default: True
       Flag to turn off writing the  JSON. Good for debugging whenm combined with `return_dict`.

    return_dict : Bool, optional, default: False
              Flag to return the output as a dictionary

    cifscantype : {"flex", "standard"}, default: "flex"
              Flag passed to `pycifrw` via :func:`~pyresid.locate_residues2`; `scantype` can be `standard` or `flex`.  `standard` provides
              pure Python parsing at the cost of a factor of 10 or so in speed.  `flex` will tokenise
              the input CIF file using fast C routines.  Note that running PyCIFRW in Jython uses
              native Java regular expressions to provide a speedup regardless of this argument.

    context : String, optional, default: "sent"
          Flag passed to :func:`~pyresid.locate_residues2` to determine the type of context added
          to annotations, "sent" uses the spaCy parsed sentences, anything else will use `x`
          characters either side of the matched tokens.

    use_actual_sections : Bool, optional, default: False
                      Flag passed to :func:`~pyresid.locate_residues2`, in order to use the actual
                      titles rather than the fuzzy matches to the EBI section whitelist.

    verbose : Bool, optional, default: False
          Flag to turn on verbose output

    Returns
    -------
    (optional) outdict: OrderedDict
         Dictionary containing the annotations. Good for debugging.

    See Also
    --------
    * :func:`~pyresid.locate_residues2`
    """

    nlp = spacy.load('en')
    outpath = os.path.join(os.path.abspath(outdir), filename)

    if isinstance(ext_id_list, str):  ## Check that the passed list is valid (if single string, parses as single ID)
        ext_id_list = [ext_id_list, ]

    outdict = {}

    for ext_id in ext_id_list:
        print("Processing", ext_id)

        text_dict = get_text(ext_id)                                ## retrieve the text
        fulltext = reconstruct_fulltext(text_dict, tokenise=False)  ## convert from sections to fulltext
        fulldoc = nlp(fulltext)                                     ## load into a spaCy doc for tokenising
        fulltext_tokens = [t for t in fulldoc]                      ## get list of tokens

        residue_mentions = identify_residues(fulltext, return_mentions=True)    ## Find residue mentions
        unique_proteins = identify_protein_ID(fulltext)                         ## find PDB structure mentions

        output_dict = locate_residues2(fulltext_tokens=fulltext_tokens, residue_mentions=residue_mentions,
                                       unique_proteins=unique_proteins,
                                       text_dict=text_dict, fulltext=fulltext, ext_id=ext_id,
                                       cifscantype=cifscantype, use_actual_sections=use_actual_sections,
                                       context=context, verbose=verbose)
        if save:
            with open(outpath, 'a') as outfile:
                json.dump(output_dict, outfile, cls=MyEncoder, separators=(',', ':'))
                outfile.write("\n")
        outdict[ext_id] = output_dict
        if verbose:
            print(output_dict)

    if return_dict:
        return outdict
    else:
        pass
    pass


def locate_residues2(fulltext_tokens, residue_mentions, text_dict, ext_id, fulltext,
                     unique_proteins, fulldoc=False, provider="West-Life", offset=True, x=50,
                     include_sentence=False, include_token=False, cifscantype="flex",
                     context="sent", use_actual_sections=False, verbose=False,):
    """

    Locate the already identified residues within tokenised fulltext.

    Parameters
    ----------
    fulltext_tokens : List of strings
                  Array of tokens to search for *residue_mentions*, typically
                  the output from :func:`~pyresid.reconstruct_fulltext`.

    residue_mentions : Set, or other iterable.
                   Typically output from :func:`~pyresid.identify_residues`,
                   the residues which to locate within *fulltext_tokens*.

    text_dict : Dict or OrderedDict
            Dictionary containing the parsed XML. Each entry corresponds to a Section
            in the XML. Usually an output from :func:`~pyresid.get_sections_text`

    ext_id : String
         ePMC identifier used to retrieve the relevant entry. Format is prefix of 'PMC'
         followed by an integer.

    fulltext :  string
                text snippet to be searched for residues.

    unique_proteins : Set, or other iterable.
                  PDB entry matches found within `fulltext` - usually an output from :func:`~pyresid.identify_protein_ID`.
    fulldoc : optional, default: False
          If a spaCy `fulldoc` is not passed, one is created using `fulltext`.

    provider : String, default: "West-Life".
           The string used to link back to the annotation proveneance. Stipulation of the EBI.

    offset : Bool, optional, default: False
         Flag to include the location index (idx) within the `location_dict`,
         value is the number of characters the start of the matched string is
         from the start of the fulltext document from which `fulltext_tokens`
         was tokenised.

    x : int, optional, default: 50
        How much context to include if context is set to something other than "sent"

    include_sentence : Bool, optional, default: False
                   Flag to set the context behaviour - will return a spaCy sentence rather than
                   raw context.

    include_token : Bool, optional, default: False
                Flag to determine whether to return the matched token in the `annsdict`

    cifscantype : {"flex", "standard"}, default: "flex"
              Flag passed to `pycifrw`; `scantype` can be `standard` or `flex`.  `standard` provides
              pure Python parsing at the cost of a factor of 10 or so in speed.  `flex` will tokenise
              the input CIF file using fast C routines.  Note that running PyCIFRW in Jython uses
              native Java regular expressions to provide a speedup regardless of this argument.

    context : String, optional, default: "sent"
          Flag passed to determine the type of context added to annotations, "sent" uses the spaCy
          parsed sentences, anything else will use *x* characters either side of the matched tokens.

    use_actual_sections : Bool, optional, default: False
                      Flag passed to use the actual titles rather than the fuzzy matches to the EBI
                      section whitelist.

    verbose : Bool, optional, default: False
          Flag to turn on verbose output


    Returns
    -------

    location_dict : OrderedDict
                Ordered dictionary containing the locations, matched string
                and frequency of each of the residue mentions passed, which
                are themselves used as the dict keys.

    See Also
    --------
    * :func:`~pyresid.identify_residues`
    * :func:`~pyresid.locate_residues`
    * `pyresid.EBI_whitelist`: list of allowed section titles for the EBI

    """

    sec_names = [text_dict[i]["title"] for i in text_dict]
    sec_offset = [text_dict[i]["offset"] for i in text_dict]

    ## preprocess mentions
    residue_mentions = preprocess_mentions(residue_mentions)

    if verbose:
        print(residue_mentions)

    if not fulldoc:
        nlp = spacy.load('en')
        fulldoc = nlp(fulltext)

    location_dict = OrderedDict()

    for i, tkn in enumerate(residue_mentions):

        ## Locate the residue within the list of tokens
        locations = [word for word in enumerate(fulltext_tokens) if
                     tkn in str(word[1])]  ## Should make it possible to pass spacy tokens
        if verbose:
            print(i, " tkn=", tkn)
            print(locations, len(locations))

        ## convert exact mentions into individual residual - this deals with hyphens and slashes
        decomposed = subdivide_compound_residues(tkn)

        ## Loop through the decomposed tokens - exact mention is the same, but the individual residue is distinct
        for newtkn in decomposed:


            where = [newtkn in identify_residues(str(word[1]), verbose=False) for word in enumerate(fulltext_tokens)]

            if verbose:
                print("newtkn=", newtkn)
                print("locations = ", np.arange(len(fulltext_tokens))[where])
                print("Strings = ", np.array(fulltext_tokens)[where])

            if newtkn not in location_dict:
                # if no key for token, make a new datastructure
                location_dict[newtkn] = OrderedDict()
                if offset:
                    location_dict[newtkn]["offset"] = []
                location_dict[newtkn]["locations"] = []
                location_dict[newtkn]["string"] = []
                location_dict[newtkn]["freq"] = 0
            else:
                #                 print("known")
                pass

            location_dict[newtkn]["locations"] = np.arange(len(fulltext_tokens))[where]
            location_dict[newtkn]["string"] = np.array(fulltext_tokens)[where]
            location_dict[newtkn]["freq"] = len(location_dict[newtkn]["locations"])

            if offset:
                location_dict[newtkn]["offset"] = [word.idx for word in location_dict[newtkn]["string"]]

    get_rawcontext(location_dict, fulltext, x=50, verbose=False)

    output_dict = OrderedDict()
    #     output_dict["pmcid"] = ext_id
    output_dict["pmcid"] = "".join(filter(str.isdigit, ext_id))
    output_dict["provider"] = provider
    output_dict["anns"] = []

    ## SETUP STRUCT ASSOCIATE
    accession_numbers = []
    struct_dict = {}

    ## Loop through PDB structures to load in the structures, to check the candidates against
    for prot_structure in unique_proteins:

        if verbose:
            print(prot_structure, end=" ")
        ## Many PDB entries can share a since UniProt accession URI
        accession_id = find_UniProt_accession(prot_structure)
        accession_numbers.append(accession_id)

        # Only do this if one is found!
        if accession_id:
            infile = os.path.join(mmCIF_dir, prot_structure + ".cif")

            # Only download if it is not known locally
            if not os.path.exists(infile):
                download_pdbfile(pdb_id=prot_structure, outfile=infile)

            # Load in the cif file to get the structure
            if cifscantype not in  {"flex", "standard"}:
                cifscantype = "flex"
            cf = load_pdbfile(prot_structure, infile=infile, cifscantype=cifscantype)

            res_seq = get_residue_sequence(cf)
            struct_dict[prot_structure] = res_seq

            if verbose:
                print("")

    unique_accession_numbers = set(accession_numbers)
    found_accession = [i for i in zip(unique_proteins, accession_numbers) if i[1]]

    for residue in location_dict:

        ## ASSOCIATE - MATCH TO STRUCT

        matched = []

        for k in found_accession:

            if verbose:
                print(k[0])

            if residue in struct_dict[k[0]]:
                if verbose:
                    print("match")
                matched.append(k[1])

        ## CHOOSE URI
        if len(matched) == 0:
            matched.append(
                "NO MATCH FOUND")  ## -ASK WHETHER TO DROP UNMATCHED - see issue #2 http://hcp004.hartree.stfc.ac.uk/RobFirth/PDB-protein-res/issues/2
        uniprot_uri = np.unique(matched)[0]  ## Do better than just choosing the first one -
        ## duplicate entry with both URI, use ML - TODO!
        ## End Association
        locations = location_dict[residue]["locations"]
        offsets = location_dict[residue]["offset"]

        for offset, location in zip(offsets, locations):
            annsdict = OrderedDict()

            annsdict["exact"] = fulltext_tokens[location]
            if include_token:
                annsdict["token"] = residue

            if context == "sent":

                for sent in fulldoc.sents:
                    if offset >= sent.start_char and offset < sent.end_char:
                        context_sent = sent

                        if include_sentence:
                            annsdict["sent"] = sent

                if verbose:
                    print(context_sent.text, annsdict["exact"].string)
                start_index = context_sent.text.index(annsdict["exact"].string)
                annsdict["prefix"] = context_sent.text[:start_index]
                annsdict["postfix"] = context_sent.text[start_index+len(annsdict["exact"].string):]

            else:

                ## gather context prefix-postfix
                annsdict["prefix"] = fulltext[offset - x:offset]
                annsdict["postfix"] = fulltext[
                                      offset + len(fulltext_tokens[location]):offset + len(fulltext_tokens[location]) + x]

            ## ID the section
            w = np.digitize(offset, sec_offset) - 1
            annsdict["section"] = sec_names[w]

            if not use_actual_sections:
                fuzzymatch = fw.process.extract(annsdict["section"], EBI_whitelist, limit=1)[0]
                annsdict["section"] = fuzzymatch[0]

            annsdict["tags"] = []

            tagdict = OrderedDict()
            # tagdict["name"] = location[1]
            #             tagdict["name"] = residue
            tagdict["name"] = uniprot_uri
            tagdict["uri"] = "https://www.uniprot.org/uniprot/" + uniprot_uri

            annsdict["tags"].append(tagdict)

            output_dict["anns"].append(annsdict)

    return output_dict


def get_currentPDBIDs(url="http://www.rcsb.org/pdb/rest/getCurrent"):
    """

    :param url:
    :return:
    """
    r = requests.get(url)

    soup = BeautifulSoup(r.text, "lxml-xml")

    return [i["structureId"] for i in soup.findAll("PDB")]


def download_pdbfile(pdb_id, outfile=None, overwrite=True):
    """

    :param pdb_id:
    :param outfile:
    :param overwrite:
    :return:
    """
    # pdb_id = '1LAF'
    # pdb_id = '4P0I'
    # pdb_file = pdb.get_pdb_file(pdb_id, filetype="mmCIF")

    if not outfile:
        outfile = os.path.join(os.path.abspath(os.curdir), pdb_id + ".cif")  ## TODO - needs to point at mmCIF dir

    if os.path.exists(outfile) and not overwrite:
        print("File already exists at", outfile)
        print("run with overwrite=True to force")
        return

    request_url = "https://files.rcsb.org/download/" + pdb_id + ".cif"
    # pdb_file
    r = requests.get(request_url)

    if r.status_code == 200:
        print("saving to", outfile)
        with open(outfile, 'w') as f:
            f.write(r.text)

        pass
    else:
        warnings.warn("request to " + str(pdb_id) + " has failed to return 200, and has returned " + str(r.status_code))
    pass


def load_struct_from_pdbfile(pdb_id, infile=None):
    """
    DEPRECATED
    :param pdb_id:
    :param infile:
    :return:
    """
    p = MMCIFParser()

    if not infile:
        infile = os.path.join(os.path.abspath(os.curdir), pdb_id + ".cif")  ## TODO - needs to point at mmCIF dir

    structure = p.get_structure(pdb_id, infile)

    return structure


def load_pdbfile(pdb_id, infile=None, cifscantype='flex'):
    """

    :param pdb_id:
    :param infile:
    :return:
    """
    if not infile:
        infile = os.path.join(mmCIF_dir, pdb_id + ".cif")

    cf = CifFile.ReadCif(infile, scantype=cifscantype)

    return cf


def get_residue_sequence(cf):
    """
    used to work with load_struct_from_pdbfile, now uses load_pdbfile output
    :param  structure:
    :return:
    """
    # residue_sequence = list(np.array([[residue.resname.capitalize(), int(residue.id[1])] for residue in
    #                                    list(structure.get_chains())[0].get_residues()]).T)

    pdb = cf.keys()[0]
    cf_mon = [s.capitalize() for s in cf[pdb]["_entity_poly_seq.mon_id"]]
    cf_num = cf[pdb]["_entity_poly_seq.num"]

    ## Identify where the chain begins (after the signal peptide)
    try:
        align_beg = int(cf[pdb]["_struct_ref_seq.db_align_beg"])  ## if only one chain
        align_beg = align_beg - 1
    except:
        align_beg = int(cf[pdb]["_struct_ref_seq.db_align_beg"][0])  ## beginning index
        align_beg = align_beg - 1

    cf_num = [str(int(i) + align_beg - 1) for i in cf_num]  ## -1 again ?

    residue_sequence = [x + y for x, y in zip(cf_mon, cf_num)]

    return residue_sequence


def get_PDB_summary(PDB_id, verbose=False):
    """
    Similar info to get_meta, but for a PDB entry - returns info about when it was regitered etc.

    Parameters
    ----------
    PDB_id :

    verbose : Bool, optional, default: False
          Flag to turn on verbose output

    Returns
    -------

    See Also
    --------
    *:func:`~pyresid.get_meta`
    """

    status = get_PDB_status(PDB_id=PDB_id, verbose=verbose)

    if status == "CURRENT":
        url = "http://www.rcsb.org/pdb/rest/describePDB?structureId=" + PDB_id
    elif status == "UNRELEASED":
        url = "http://www.rcsb.org//pdb/rest/getUnreleased?structureId=" + PDB_id
    else:
        print("Do not recognise status", status)
        return False

    r = requests.get(url)
    if r.status_code == 200:

        soup = BeautifulSoup(r.text, "lxml-xml")

        if status == "CURRENT":
            attrs_dict = soup.find("PDB").attrs

            if hasattr(soup.find("PDB"), "contents"):
                contents = [i for i in soup.find("PDB").contents if i != "\n"]
                for item in contents:

                    if item.name not in attrs_dict:
                        attrs_dict[item.name] = []
                    if "pdbId" in item.attrs:
                        attrs_dict[item.name].append(item.attrs["pdbId"])
                    else:
                        attrs_dict[item.name].append(item.attrs)

            else:
                if verbose:
                    print("No contents")

        elif status == "UNRELEASED":
            attrs_dict = soup.find("record").attrs

            if hasattr(soup.find("record"), "contents"):

                contents = [i for i in soup.find("record").contents if i != "\n"]

                for item in contents:
                    if verbose:
                        print(item.name)

                    if len(item.attrs) > 0:
                        for key in item.attrs:
                            attrs_dict[key] = item.attrs[key]
                    if len(item.contents) > 0:
                        attrs_dict[item.name] = item.contents

            else:
                if verbose:
                    print("No contents")

        return attrs_dict

    else:
        warnings.warn("request to " + str(PDB_id) + " has failed to return 200, and has returned " + str(r.status_code))
    pass


def get_PDB_status(PDB_id, verbose=False):
    """
    Check status (released/unreleased etc.) of PDB

    Parameters
    ----------
    PDB_id :

    verbose : Bool, optional, default: False
          Flag to turn on verbose output

    Returns
    -------

    """

    # PDB_id = "4POW"
    url = "http://www.rcsb.org/pdb/rest/idStatus?structureId=" + PDB_id
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml-xml")

    status = soup.record["status"]

    if verbose:
        print(status)

    return status


def get_annotations(ext_id):
    """

    Parameters
    ----------
    ext_id

    Returns
    -------

    """
    url = "https://www.ebi.ac.uk/europepmc/annotations_api/annotationsByArticleIds?articleIds="
    request_url = url + "PMC:" + ext_id
    r = requests.get(request_url)
    annotations = json.loads(r.text)[0]

    return annotations


def get_accession_numbers(annotations=None, ext_id=None):
    """

    Parameters
    ----------
    annotations
    ext_id

    Returns
    -------

    """
    if not annotations:
        annotations = get_annotations(ext_id)

    pdb_ids = list(set([anno["exact"] for anno in annotations["annotations"] if anno["type"] == "Accession Numbers"]))
    return pdb_ids


def find_UniProt_accession(pdb_id, verbose=False):
    """
    Note - returns the first hit acc num, which should be the one that corresponds to the "recommended name"

    :param pdb_id:
    :param verbose:
    :return:
    """

    request_url = r"https://www.uniprot.org/uniprot/?query=database:(type:pdb " + pdb_id + ")&format=xml"

    r = requests.get(request_url)
    soup = BeautifulSoup(r.text, "lxml-xml")

    if soup.find("accession"):
        first_hit_URI = soup.find("accession").text
    else:
        print("accession not found for", pdb_id)
        first_hit_URI = False

    if verbose:
        print(first_hit_URI)

    return (first_hit_URI)


def check_loc_dict(loc_dict):
    for res in loc_dict:
        print(res)
        freq = loc_dict[res]["freq"]
        n_offset = len(loc_dict[res]["offset"])
        n_locations = len(loc_dict[res]["locations"])
        print(freq, n_offset, n_locations)


if __name__ == "__main__":
    pass
else:
    pass
