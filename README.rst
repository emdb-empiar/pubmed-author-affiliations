==========================
pubmed-author-affiliations
==========================
Command line tool the takes one or a list of Pubmed IDs or DOIs,
searches Pubmed for corresponding author affiliations and 
outputs the information to file


Command line options
--------------------
-h, --help                        Show help text
-i PUBMEDID, --pubmedid PUBMEDID  Search for author affiliations for single Pubmed ID
-d doi, --doi doi                 Search for author affiliations for a single DOI
-f file, --infile file            File with a list of Pubmed IDs and DOIs (they can be mixed). One entry per line.
-x format, --format format        Output format. Choices=['json' (default),'text']. 'text' option produces tab separated
                                  table, denormalised in the sense that the pubmed ID/DOI is repeated on multiple rows
                                  if there are multiple authors with related affiliations.

Example runs
------------
Pubmed input and JSON output:
.. code:: bash
    python pubmedAuthorAffiliation.py -i 27863242

Output::
    {'articleTitle': 'Decoding Mammalian Ribosome-mRNA States by Translational GTPase Complexes.', 'journalTitle': 'Cell', 'authorList': [{'firstName': 'n/a', 'institute': 'MRC-LMB', 'lastName': 'Shao', 'affiliation': 'MRC-LMB, Francis Crick Avenue, Cambridge CB2 0QH, UK.', 'country': 'UK', 'initials': 'S'}, {'firstName': 'n/a', 'institute': 'MRC-LMB', 'lastName': 'Murray', 'affiliation': 'MRC-LMB, Francis Crick Avenue, Cambridge CB2 0QH, UK.', 'country': 'UK', 'initials': 'J'}, {'firstName': 'n/a', 'institute': 'MRC-LMB', 'lastName': 'Brown', 'affiliation': 'MRC-LMB, Francis Crick Avenue, Cambridge CB2 0QH, UK.', 'country': 'UK', 'initials': 'A'}, {'firstName': 'n/a', 'institute': 'University of California', 'lastName': 'Taunton', 'affiliation': 'Department of Cellular and Molecular Pharmacology, University of California, San Francisco, San Francisco, CA 94158, USA.', 'country': 'USA', 'initials': 'J'}, {'firstName': 'n/a', 'institute': 'MRC-LMB', 'lastName': 'Ramakrishnan', 'affiliation': 'MRC-LMB, Francis Crick Avenue, Cambridge CB2 0QH, UK. Electronic address: ramak@mrc-lmb.cam.ac.uk.', 'country': 'UK', 'initials': 'V'}, {'firstName': 'n/a', 'institute': 'MRC-LMB', 'lastName': 'Hegde', 'affiliation': 'MRC-LMB, Francis Crick Avenue, Cambridge CB2 0QH, UK. Electronic address: rhegde@mrc-lmb.cam.ac.uk.', 'country': 'UK', 'initials': 'RS'}], 'pubmedId': '27863242', 'error': False}
    {'articleTitle': 'Decoding Mammalian Ribosome-mRNA States by Translational GTPase Complexes.', 'journalTitle': 'Cell', 'authorList': [{'firstName': 'n/a', 'institute': 'MRC-LMB', 'lastName': 'Shao', 'affiliation': 'MRC-LMB, Francis Crick Avenue, Cambridge CB2 0QH, UK.', 'country': 'UK', 'initials': 'S'}, {'firstName': 'n/a', 'institute': 'MRC-LMB', 'lastName': 'Murray', 'affiliation': 'MRC-LMB, Francis Crick Avenue, Cambridge CB2 0QH, UK.', 'country': 'UK', 'initials': 'J'}, {'firstName': 'n/a', 'institute': 'MRC-LMB', 'lastName': 'Brown', 'affiliation': 'MRC-LMB, Francis Crick Avenue, Cambridge CB2 0QH, UK.', 'country': 'UK', 'initials': 'A'}, {'firstName': 'n/a', 'institute': 'University of California', 'lastName': 'Taunton', 'affiliation': 'Department of Cellular and Molecular Pharmacology, University of California, San Francisco, San Francisco, CA 94158, USA.', 'country': 'USA', 'initials': 'J'}, {'firstName': 'n/a', 'institute': 'MRC-LMB', 'lastName': 'Ramakrishnan', 'affiliation': 'MRC-LMB, Francis Crick Avenue, Cambridge CB2 0QH, UK. Electronic address: ramak@mrc-lmb.cam.ac.uk.', 'country': 'UK', 'initials': 'V'}, {'firstName': 'n/a', 'institute': 'MRC-LMB', 'lastName': 'Hegde', 'affiliation': 'MRC-LMB, Francis Crick Avenue, Cambridge CB2 0QH, UK. Electronic address: rhegde@mrc-lmb.cam.ac.uk.', 'country': 'UK', 'initials': 'RS'}], 'pubmedId': '27863242', 'error': False}

DOI input and text output::
    python pubmedAuthorAffiliation.py -d 10.1016/j.molcel.2016.11.013 -x text

Output::
    27867008	Molecular cell	Molecular Structures of Transcribing RNA Polymerase I.	n/a	L	Tafur	European Molecular Biology Laboratory (EMBL), Structural and Computational Biology Unit, Meyerhofstrasse 1, 69117 Heidelberg, Germany.	Germany	European Molecular Biology Laboratory (EMBL)
    27867008	Molecular cell	Molecular Structures of Transcribing RNA Polymerase I.	n/a	Y	Sadian	European Molecular Biology Laboratory (EMBL), Structural and Computational Biology Unit, Meyerhofstrasse 1, 69117 Heidelberg, Germany.	Germany	European Molecular Biology Laboratory (EMBL)
    27867008	Molecular cell	Molecular Structures of Transcribing RNA Polymerase I.	n/a	NA	Hoffmann	European Molecular Biology Laboratory (EMBL), Structural and Computational Biology Unit, Meyerhofstrasse 1, 69117 Heidelberg, Germany.	Germany	European Molecular Biology Laboratory (EMBL)
    27867008	Molecular cell	Molecular Structures of Transcribing RNA Polymerase I.	n/a	AJ	Jakobi	European Molecular Biology Laboratory (EMBL), Structural and Computational Biology Unit, Meyerhofstrasse 1, 69117 Heidelberg, Germany; European Molecular Biology Laboratory (EMBL), Hamburg Unit, Notkestrasse 85, 22607 Hamburg, Germany.	Germany	European Molecular Biology Laboratory (EMBL)
    27867008	Molecular cell	Molecular Structures of Transcribing RNA Polymerase I.	n/a	R	Wetzel	European Molecular Biology Laboratory (EMBL), Structural and Computational Biology Unit, Meyerhofstrasse 1, 69117 Heidelberg, Germany.	Germany	European Molecular Biology Laboratory (EMBL)
    27867008	Molecular cell	Molecular Structures of Transcribing RNA Polymerase I.	n/a	WJH	Hagen	European Molecular Biology Laboratory (EMBL), Structural and Computational Biology Unit, Meyerhofstrasse 1, 69117 Heidelberg, Germany.	Germany	European Molecular Biology Laboratory (EMBL)
    27867008	Molecular cell	Molecular Structures of Transcribing RNA Polymerase I.	n/a	C	Sachse	European Molecular Biology Laboratory (EMBL), Structural and Computational Biology Unit, Meyerhofstrasse 1, 69117 Heidelberg, Germany.	Germany	European Molecular Biology Laboratory (EMBL)
    27867008	Molecular cell	Molecular Structures of Transcribing RNA Polymerase I.	n/a	CW	Müller	European Molecular Biology Laboratory (EMBL), Structural and Computational Biology Unit, Meyerhofstrasse 1, 69117 Heidelberg, Germany. Electronic address: cmueller@embl.de.	Germany	European Molecular Biology Laboratory (EMBL)

Input file with mixed DOI and Pubmed. Text output written to a file::
    python pubmedAuthorAffiliation.py -f emdb-2010.txt -x text > /tmp/out.txt

In this case unrecognized lines are ignored, e.g.::
    WARNING:root:processList: id not recognized: id

Code testing
------------
This will go through lists of selected Pubmed and DOI known to work::
    python test_pubmedAuthorAffiliation.py
