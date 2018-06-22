#!/usr/bin/env python
"""
test_emdbAuthorAffiliation.py

Test emdbAuthorAffiliation

2016/12/14, Ardan Patwardhan, EMBL-EBI

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
from emdbAuthorAffiliation import EmdbAuthorAffiliation
import logging
import unittest

class TestEmdbAuthorAffiliation(unittest.TestCase):
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
        emdbAuthorAffiliation = EmdbAuthorAffiliation()
        logging.info('Processing pubmed ID queries')
        for pmid in self.pubmedEntries:
            logging.info('Pubmed ID: %s' % pmid)
            logging.info('JSON output')
            jsonOut = emdbAuthorAffiliation.entrezQuery(pmid)
            logging.info(jsonOut) 
            logging.info('Text output')
            textOut = emdbAuthorAffiliation.json2Text(jsonOut)
            logging.info(textOut)
        
        logging.info('Processing DOI queries')    
        for doi in self.doiEntries:           
            logging.info('DOI: %s' % doi)
            logging.info('JSON output')
            jsonOut = emdbAuthorAffiliation.entrezQuery(doi=doi)
            logging.info(jsonOut) 
            logging.info('Text output')
            textOut = emdbAuthorAffiliation.json2Text(jsonOut)
            logging.info(textOut)   
            

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()