#!/usr/bin/env python
"""
test_pubmedAuthorAffiliation.py

Test pubmedAuthorAffiliation with set lists of Pubmed IDs and DOIs

2016/12/14, Ardan Patwardhan, EMBL-EBI

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
from pubmedAuthorAffiliation import CitationAuthorAffiliation
import logging
import unittest


class TestPubmedAuthorAffiliation(unittest.TestCase):
    """
    Find affiliation info for a test set of punmed and doi codes
    """
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.pubmedEntries = ['27863242', '27872205', '27818103', '9548720', '14526082']
        self.doiEntries = ['10.1016/j.molcel.2016.11.013']
        
    def testQueries(self):
        """
            Make test queries to pubmed 
        """
        emdb_author_affiliation = CitationAuthorAffiliation()
        logging.info('Processing pubmed ID queries')
        for pmid in self.pubmedEntries:
            logging.info('Pubmed ID: %s' % pmid)
            logging.info('JSON output')
            json_out = emdb_author_affiliation.entrez_query(pmid)
            logging.info(json_out)
            logging.info('Text output')
            text_out = emdb_author_affiliation.json2text(json_out)
            logging.info(text_out)
        
        logging.info('Processing DOI queries')    
        for doi in self.doiEntries:           
            logging.info('DOI: %s' % doi)
            logging.info('JSON output')
            json_out = emdb_author_affiliation.entrez_query(doi=doi)
            logging.info(json_out)
            logging.info('Text output')
            text_out = emdb_author_affiliation.json2text(json_out)
            logging.info(text_out)
            

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()