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
-d doi               Search for author affiliations for a single DOI
--doi doi            Same as ``-d``
-f file              File with a list of Pubmed IDs and DOIs (they can be mixed). One entry per line.
--infile file        Same as ``-f``
-x format            Output format. Choices=['json','text']. 'text' option produces tab separated table, denormalised
                     in the sense that the pubmed ID/DOI is repeated on multiple rows if there are multiple authors with
                     related affiliations.
--format format      Same as ``-x``