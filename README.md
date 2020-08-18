# ML-for-MDM
Exploring how we can improve Master Data Management (MDM) systems using machine learning. 
Presently, MDM systems leverage match and merge logic which relies on pre-written, deterministic rules to identify record linkages. 
In this repository, I explore how this deterministic logic can be supplemented with open source ML resources such as python's dedupe.

First, I created a script that leverages pydbgen to randomly generate records (name, address*, identifiers, etc.) with data quality issues that one might observe in a
MDM system such as NULLs, typographical errors, etc. (generate_MDM_data.py). The goal with these records was to create multiple records that in reality correspond
to the same entity and to see if it would be possible that despite the data quality issues one can identify groupings of records that
correspond to the same entity.

Second, I leveraged python's dedupe to train a classification model as well as a clustering model on this task. For this, there was no
support for training models off of a csv file, so I created a function to do so (MDM_dedupe.py).

And finally, I created a means of evaluating how well the clustering performed (evaluate_dedupe.py). Ultimately, this initial POC achieved majority cluster 
identification rate of 71%.

*address abbreviations were taken from USPS website (https://pe.usps.com/text/pub28/28apc_002.htm)
