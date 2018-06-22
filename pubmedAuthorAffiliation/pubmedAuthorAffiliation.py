#!/usr/bin/env python
"""
pubmedAuthorAffiliation.py

Search PUBMED for affiliation information for authors associated with citations specified as Pubmed IDs or DOIs

2016/12/13, Ardan Patwardhan, EMBL-EBI

TODO:

Version history:


                                                                                  
Copyright [2014-2018] EMBL - European Bioinformatics Institute
Licensed under the Apache License, Version 2.0 (the
"License"); you may not use this file except in
compliance with the License. You may obtain a copy of
the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied. See the License for the
specific language governing permissions and limitations
under the License.
"""
__author__ = 'Ardan Patwardhan'

import argparse
import urllib
import urllib2
from lxml import etree
import json
import logging
import re
import traceback


class CitationAuthorAffiliation:
    
    entrezEutilsEfetch = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'
    entrezEutilsEsearch = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    pubmed = 'pubmed'
    pubmed_pat = re.compile(r'(^|\s+)(\d{1,})($|\s+)')
    doi_pat = re.compile(r'(DOI:)?(10.\d{4,9}/[-._;()/:A-Z0-9]+)', re.IGNORECASE)
    country_pat = re.compile(r'^[\s]*([A-Z][\sA-Z]+)($|[.\s])', re.IGNORECASE)
    textOutputFormat = '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s'
    outputFormatChoices = ['json', 'text']
    na = 'n/a'
    
    def __init__(self):
        self.outputFormat = 'json'
        
    def set_output_format(self, fmt):
        if fmt in self.outputFormatChoices:
            self.outputFormat = fmt
        else:
            logging.warning('setOutputFormat: Unknown format ignored (default: json): %s' % fmt)
    
    def json2text(self, json_input):
        """
        Convert JSON representation to text (denormalized table with one line for each author)
        
        Parameters:
        @return: multi-line string in the format: self.textOutputFormat % (pubmedId, journalTitle, articleTitle,
                 firstName, initials, lastName, affiliation, country, institute)
        """
        pubmed_id = json_input['pubmedId']
        journal_title = json_input['journalTitle']
        article_title = json_input['articleTitle']
        lines = []
        for author in json_input['authorList']:
            first_name = author['firstName']
            last_name = author['lastName']
            initials = author['initials']
            affiliation = author['affiliation']
            country = author['country']
            institute = author['institute']
            lines.append(self.textOutputFormat % (pubmed_id, journal_title, article_title, first_name, initials,
                                                  last_name, affiliation, country, institute))
            
        return u'\n'.join(lines).encode('utf-8')
    
    def print_result(self, json_input):
        """
        Convert jsonInput to appropriate output format and print
        
        Parameters:
        @param json_input: input json that is to be converted
        """
        if self.outputFormat == 'json':
            print json_input
        elif self.outputFormat == 'text':
            print self.json2text(json_input)

    def entrez_query(self, pubmed_id=None, doi=None):
        """
        Search pubmed database for affiliation information based on provided ID and return a JSON with relevant info
        
        Parameters:
        @param pubmed_id:    PubMed ID to fetch information for
        @param doi:    Document identifier (DOI) to fetch information for 
        """
        ret_json = {'error': False}
        if doi is not None:
            # Fetch pubmed ID from pubmed
            doi_url = self.entrezEutilsEsearch
            doi_values = {
                      'term': "%s" % doi,
                      'db': self.pubmed,
                      'retmode': 'json'
                      }
            doi_url_data = urllib.urlencode(doi_values)
            # When I try doing the following as a POST rather than GET, the urlopen fails...
            doi_req = urllib2.Request(doi_url + '?' + doi_url_data)
            try:
                doi_response = urllib2.urlopen(doi_req)
            except urllib2.URLError, e:
                logging.warning('entrezQuery: error with doi search request: %s' % ('URLError = ' + str(e.reason)))
                ret_json['error'] = True
                return ret_json
            except Exception:
                logging.warning('entrezQuery: error with doi search request: %s' % traceback.format_exc())
                ret_json['error'] = True
                return ret_json
            json_response = json.loads(doi_response.read())
            if int(json_response['esearchresult']['count']) > 0:
                pubmed_id = json_response['esearchresult']['idlist'][0]
            else:
                logging.warning('entrezQuery: Unable to get pubmed ID from DOI: %s' % doi)
                ret_json['error'] = True
                return ret_json
            
        ret_json['pubmedId'] = pubmed_id
        url = self.entrezEutilsEfetch
        values = {
                  'id': pubmed_id,
                  'db': self.pubmed,
                  'retmode': 'xml'
                  }
        url_data = urllib.urlencode(values)
        req = urllib2.Request(url, url_data)
        try:
            response = urllib2.urlopen(req)
        except urllib2.URLError, e:
            logging.warning('entrezQuery: error with pubmed fetch request: %s' % ('URLError = ' + str(e.reason)))
            ret_json['error'] = True
            return ret_json
        except Exception:
            logging.warning('entrezQuery: error with pubmed fetch request: %s' % traceback.format_exc())
            ret_json['error'] = True
            return ret_json
        xml_response = response.read()
        xml_root = etree.fromstring(xml_response)
        
        journal_title_tag_list = xml_root.xpath('//Article/Journal/Title')
        if journal_title_tag_list is not None and len(journal_title_tag_list) > 0:
            ret_json['journalTitle'] = journal_title_tag_list[0].text
        else:
            ret_json['journalTitle'] = self.na

        article_title_tag_list = xml_root.xpath('//Article/ArticleTitle')
        if article_title_tag_list is not None and len(article_title_tag_list) > 0:
            ret_json['articleTitle'] = article_title_tag_list[0].text
        else:
            ret_json['articleTitle'] = self.na
        
        # Get only authors that have an associated affiliation
        author_tag_list = xml_root.xpath('//AuthorList/Author[AffiliationInfo/Affiliation]')
        author_list = []
        for authorTag in author_tag_list:
            author = {'firstName': self.na, 'initials': self.na, 'lastName': self.na, 'affiliation': self.na,
                      'country': self.na, 'institute': self.na}
            for elem in authorTag:
                if elem.tag == 'LastName':
                    author['lastName'] = elem.text
                if elem.tag == 'FirstName':
                    author['firstName'] = elem.text   
                if elem.tag == 'Initials':
                    author['initials'] = elem.text 
                if elem.tag == 'AffiliationInfo':
                    x = (elem.xpath('Affiliation')[0]).text
                    author['affiliation'] = x
                    y = x.split(',')
                    match = self.country_pat.search(y[-1])
                    if match:
                        groups = match.groups()
                        if len(groups) > 0:
                            author['country'] = groups[0]
                        else:
                            author['country'] = self.na

                    # Find the primary institution details
                    # It is not clear which field this is so we search for key words in order
                    xlc = x.lower()
                    search_terms = ['universi',  # in France and Spain the endings are different from English
                                    'institut',
                                    'mrc-lmb', 'ebi', 'embl-ebi', 'embl', 'riken', 'academy', 'college', 'laboratory',
                                    'school']
                    search_ref = None
                    for term in search_terms:
                        if re.search(term, xlc):
                            search_ref = term
                            break
                    if search_ref is not None:
                        for field in y:
                            if re.search(search_ref, field, re.IGNORECASE):
                                author['institute'] = field.lstrip(' ')
                                break
                    else:
                        author['institute'] = 'Unparsed'
                else:
                    author['affiliation'] = self.na
                    author['country'] = self.na
                    author['institute'] = self.na

            author_list.append(author)
        ret_json['authorList'] = author_list
                    
        return ret_json

    def process_list(self, infile):
        """
        Go through a list of ids (can be pubmed and doi mixed) and find affiliations
        
        Parameters
        @param infile: File with PUBMED and DOI accessions. One ID is expected on each line. Lines that cannot be parsed
                       are ignored
        """
        infd = open(infile, 'r')
        for line in infd:
            found = False
            # ignore lines that do not correspond to a valid pubmed id or a doi
            match = self.pubmed_pat.search(line)
            if match:
                groups = match.groups()
                if len(groups) > 1:
                    pubmedid = groups[1]
                    json_out = self.entrez_query(pubmedid)
                    found = True
                    if json_out['error'] is True:
                        logging.warning('processList: Unable to process pubmed ID: %s' % pubmedid)
                    else:
                        self.print_result(json_out)
                   
            else:
                match = self.doi_pat.search(line)
                if match:
                    groups = match.groups()
                    if len(groups) > 1:
                        doi = groups[1]
                        json_out = self.entrez_query(doi=doi)
                        found = True
                        if json_out['error'] is True:
                            logging.warning('processList: Unable to process doi: %s' % doi)
                        else:
                            self.print_result(json_out)
                        
            if not found:
                logging.warning('processList: id not recognized: %s' % line)


def main():
    """
    Search PUBMED for affiliation information for authors associated with EMDB entries

    """
    
    # Handle command line options
    description = """
            pubmedAuthorAffiliation.py [options] 
            Search PUBMED for affiliation information about authors and print out the information.
            This program takes PUBMED IDs or DOI to fetch the information from the PUBMED archive.
            You can either specify a single ID on the command line or a file which contains a list.

            Examples:
            1) Run unit tests
                python pubmedAuthorAffiliation.py --test 

            Typical run:
            python emdb_xml_translate.py -f out.xml -i 1.9 -o 2.0 in.xml
            in.xml is assumed to be a EMDB 1.9 XML file and converted to 
            an XML file following EMDB XML schema 2.0 and written out to out.xml
               
            """
    version = "0.2"
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--pubmedid", help="Pubmed ID")
    parser.add_argument("-d", "--doi", help="DOI")
    parser.add_argument("-f", "--infile", help="Text file with a list of pubmed/doi (they can be mixed)")
    parser.add_argument("-x", "--format", choices=CitationAuthorAffiliation.outputFormatChoices, help="Format of output. Options json, text (tab separated table, denormalised in the sense that the pubmed ID is repeated on multiple rows if there are multiple authors with affiliations")
    args = parser.parse_args()

    citation_author_affiliation = CitationAuthorAffiliation()
    if args.format:
        citation_author_affiliation.set_output_format(args.format)
    if args.pubmedid:        
        json_out = citation_author_affiliation.entrez_query(args.pubmedid)
        citation_author_affiliation.print_result(json_out)
        print json_out
    elif args.doi:
        json_out = citation_author_affiliation.entrez_query(doi=args.doi)
        citation_author_affiliation.print_result(json_out)
    elif args.infile:
        citation_author_affiliation.process_list(args.infile)
        

if __name__ == "__main__":
    main()