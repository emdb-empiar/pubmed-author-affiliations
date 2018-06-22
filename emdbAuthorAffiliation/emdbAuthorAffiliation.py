#!/usr/bin/env python
"""
emdbAuthorAffiliation.py

Search PUBMED for affiliation information for authors associated with EMDB entries

2016/12/13, Ardan Patwardhan, EMBL-EBI

TODO:

Version history:


                                                                                  
Copyright [2014-2016] EMBL - European Bioinformatics Institute
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
import argparse
import urllib
import urllib2
from lxml import etree
import json
import logging
import re
import traceback



class EmdbAuthorAffiliation():
    
    entrezEutilsEfetch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
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
        
    def setOutputFormat(self, fmt):
        if fmt in self.outputFormatChoices:
            self.outputFormat = fmt
        else:
            logging.warning('setOutputFormat: Unknown format ignored (default: json): %s' % fmt)
    
    def json2Text(self, jsonInput):
        """
        Convert JSON representation to text (denormalized table with one line for each author)
        
        Parameters:
        @return: multi-line string in the format: self.textOutputFormat % (pubmedId, journalTitle, articleTitle, firstName, initials, lastName, affiliation, country, institute)
        """
        pubmedId = jsonInput['pubmedId']
        journalTitle = jsonInput['journalTitle']
        articleTitle = jsonInput['articleTitle']
        lines = []
        for author in jsonInput['authorList']:
            firstName = author['firstName']
            lastName = author['lastName']
            initials = author['initials']
            affiliation = author['affiliation']
            country = author['country']
            institute = author['institute']
            lines.append(self.textOutputFormat % (pubmedId, journalTitle, articleTitle, firstName, initials, lastName, affiliation, country, institute))
            
        return u'\n'.join(lines).encode('utf-8')
    
    def printResult(self, jsonInput):
        """
        Convert jsonInput to appropriate output format and print
        
        Parameters:
        @param jsonInput: input json that is to be converted
        """
        if self.outputFormat == 'json':
            print jsonInput
        elif self.outputFormat == 'text':
            print self.json2Text(jsonInput)


    def entrezQuery(self, pubmedId=None, doi=None):
        """
        Search pubmed database for affiliation information based on provided ID and return a JSON with relevant info
        
        Parameters:
        @param pubmedId:    PubMed ID to fetch information for
        @param doi:    Document identifier (DOI) to fetch information for 
        """
        retJson = {'error': False}
        if doi is not None:
            # Fetch pubmed ID from pubmed
            doiUrl = self.entrezEutilsEsearch
            doiValues = {
                      'term': "%s" % doi,
                      'db': self.pubmed,
                      'retmode': 'json'
                      }
            doiUrlData = urllib.urlencode(doiValues)
            # When I try doing the following as a POST rather than GET, the urlopen fails...
            doiReq = urllib2.Request(doiUrl + '?' + doiUrlData)
            try:
                doiResponse = urllib2.urlopen(doiReq)
            except urllib2.URLError, e:
                logging.warning('entrezQuery: error with doi search request: %s' % ('URLError = ' + str(e.reason)))
                retJson['error'] = True
                return retJson
            except Exception:
                logging.warning('entrezQuery: error with doi search request: %s' % traceback.format_exc())
                retJson['error'] = True
                return retJson
            jsonResponse = json.loads(doiResponse.read())
            if int(jsonResponse['esearchresult']['count']) > 0:
                pubmedId = jsonResponse['esearchresult']['idlist'][0]
            else:
                logging.warning('entrezQuery: Unable to get pubmed ID from DOI: %s' % doi )
                retJson['error'] = True
                return retJson
            
        retJson['pubmedId'] = pubmedId
        url = self.entrezEutilsEfetch
        values = {
                  'id': pubmedId,
                  'db': self.pubmed,
                  'retmode': 'xml'
                  }
        urlData = urllib.urlencode(values)
        req = urllib2.Request(url, urlData)
        try:
            response = urllib2.urlopen(req)
        except urllib2.URLError, e:
            logging.warning('entrezQuery: error with pubmed fetch request: %s' % ('URLError = ' + str(e.reason)))
            retJson['error'] = True
            return retJson
        except Exception:
            logging.warning('entrezQuery: error with pubmed fetch request: %s' % traceback.format_exc())
            retJson['error'] = True
            return retJson
        xmlResponse = response.read()
        xmlRoot = etree.fromstring(xmlResponse)
        
        journalTitleTagList = xmlRoot.xpath('//Article/Journal/Title')
        if journalTitleTagList is not None and len(journalTitleTagList) > 0:
            retJson['journalTitle'] = journalTitleTagList[0].text
        else:
            retJson['journalTitle'] = self.na

        articleTitleTagList = xmlRoot.xpath('//Article/ArticleTitle')
        if articleTitleTagList is not None and len(articleTitleTagList) > 0:    
            retJson['articleTitle'] = articleTitleTagList[0].text
        else:
            retJson['articleTitle'] = self.na
        
        # Get only authors that have an associated affiliation
        authorTagList = xmlRoot.xpath('//AuthorList/Author[AffiliationInfo/Affiliation]')
        authorList = []
        for authorTag in authorTagList:
            author = {}
            author['firstName'] = self.na
            author['initials'] = self.na
            author['lastName'] = self.na
            author['affiliation'] = self.na
            author['country'] = self.na
            author['institute'] = self.na
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
                    searchTerms = ['universi', # in France and Spain the endings are different from English
                                   'institut', 
                                   'mrc-lmb', 'ebi', 'embl-ebi', 'embl', 'riken', 'academy', 'college', 'laboratory', 'school']
                    searchRef = None
                    for term in searchTerms:
                        if re.search(term, xlc):
                            searchRef = term
                            break
                    if searchRef is not None:
                        for field in y:
                            if re.search(searchRef, field, re.IGNORECASE):
                                author['institute'] = field.lstrip(' ')
                                break
                    else:
                        author['institute'] = 'Unparsed'
                else:
                    author['affiliation'] = self.na
                    author['country'] = self.na
                    author['institute'] = self.na
                            
                        
            authorList.append(author)
        retJson['authorList'] = authorList    
                    
        return retJson
        
        
    def processList(self, infile):
        """
        Go through a list of ids (can be pubmed and doi mixed) and find affiliations
        
        Parameters
        @param infile: File with PUBMED and DOI accessions. One ID is expected on each line. Lines that cannot be parsed are ignored
        """
        infd = open(infile,'r')
        for line in infd:
            found = False
            # ignore lines that do not correspond to a valid pubmed id or a doi
            match = self.pubmed_pat.search(line)
            if match:
                groups = match.groups()
                if len(groups) > 1:
                    pubmedid = groups[1]
                    jsonOut = self.entrezQuery(pubmedid)
                    found = True
                    if jsonOut['error'] == True:
                        logging.warning('processList: Unable to process pubmed ID: %s' % pubmedid)
                    else:
                        self.printResult(jsonOut)
                   
            else:
                match = self.doi_pat.search(line)
                if match:
                    groups = match.groups()
                    if len(groups) > 1:
                        doi = groups[1]
                        jsonOut = self.entrezQuery(doi = doi)
                        found = True
                        if jsonOut['error'] == True:
                            logging.warning('processList: Unable to process doi: %s' % doi)
                        else:
                            self.printResult(jsonOut)
                        
            if not found:
                logging.warning('processList: id not recognized: %s' % line)


            

def main():
    """
    Search PUBMED for affiliation information for authors associated with EMDB entries

    """
    
    # Handle command line options
    description = """
            emdbAuthorAffiliation.py [options] 
            Search PUBMED for affiliation information about authors and print out the information.
            This program takes PUBMED IDs or DOI to fetch the information from the PUBMED archive.
            You can either specify a single ID on the command line or a file which contains a list.

            Examples:
            1) Run unit tests
                python emdbAuthorAffiliation.py --test 

            Typical run:
            python emdb_xml_translate.py -f out.xml -i 1.9 -o 2.0 in.xml
            in.xml is assumed to be a EMDB 1.9 XML file and converted to 
            an XML file following EMDB XML schema 2.0 and written out to out.xml
               
            """
    version = "0.1"
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--pubmedid", help="Pubmed ID")
    parser.add_argument("-d", "--doi", help="DOI")
    parser.add_argument("-f", "--infile", help="Text file with a list of pubmed/doi (they can be mixed)")
    parser.add_argument("-x", "--format", choices=EmdbAuthorAffiliation.outputFormatChoices, help="Format of output. Options json, text (tab separated table, denormalised in the sense that the pubmed ID is repeated on multiple rows if there are multiple authors with affiliations")
    args = parser.parse_args()
    """
    parser = argparse.ArgumentParser(description= description)
    parser.add_argument( '-u','--ump', action='store_true', help='Run tests.')
    args = parser.parse_args()

    
    parser = OptionParser(usage = usage, version = version)
    parser.add_option("-t", "--test", action="store", type="string", metavar="SCHEMA", dest="inputSchema", default = "1.9", help="Schema version of output file - 1.9 or 2.0 [default: %default]")
    
    parser.add_option("-o", "--out-schema", action="store", type="string", metavar="SCHEMA", dest="outputSchema", default = "2.0", help="Schema version of output file - 1.9 or 2.0 [default: %default]")
    parser.add_option("-f", "--out-file", action="store", type="string", metavar="FILE", dest="outputFile", help="Write output to FILE")
    parser.add_option("-w", "--warning-level", action="store", type="int", dest="warningLevel", default=1, help="Level of warning output. 0 is none, 3 is max, default = 1")
    (options, args) = parser.parse_args()

    # Check for sensible/supported options
    if len(args) < 1:
        sys.exit("No input file specified!")
    else:
        inputFile = args[0]
    if (options.inputSchema != "1.9" and options.outputSchema != "2.0") and (options.inputSchema != "2.0" and options.outputSchema != "1.9"):
        sys.exit("Conversion from version %s to %s not supported!" % (options.inputSchema, options.outputSchema))   
        
    # Call appropriate conversion routine
    translator = EMDBXMLTranslator()
    translator.setWarningLevel(options.warningLevel)
    if (options.inputSchema == "1.9" and options.outputSchema == "2.0"):
        translator.translate_1_9_to_2_0(inputFile, options.outputFile)
    elif (options.inputSchema == "1.9" and options.outputSchema == "1.9"):
        translator.translate_1_9_to_1_9(inputFile, options.outputFile)
    elif (options.inputSchema == "2.0" and options.outputSchema == "1.9"):
        translator.translate_2_0_to_1_9(inputFile, options.outputFile)
    
    if args.ump == True:
        logging.basicConfig(level=logging.DEBUG)
        unittest.main()
    """
    emdbAuthorAffiliation = EmdbAuthorAffiliation()
    if args.format:
        emdbAuthorAffiliation.setOutputFormat(args.format) 
    if args.pubmedid:        
        jsonOut = emdbAuthorAffiliation.entrezQuery(args.pubmedid)
        emdbAuthorAffiliation.printResult(jsonOut)
        print jsonOut
    elif args.doi:
        jsonOut = emdbAuthorAffiliation.entrezQuery(doi=args.doi)
        emdbAuthorAffiliation.printResult(jsonOut)
    elif args.infile:
        emdbAuthorAffiliation.processList(args.infile)
        

if __name__ == "__main__":
    main()