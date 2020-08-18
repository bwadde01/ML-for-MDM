# ML-for-MDM
Exploring how we can improve Master Data Management (MDM) systems using machine learning. 
Presently, MDM systems leverage match and merge logic which relies on pre-written, deterministic rules to identify record linkages. 
In this repository, I explore how this deterministic logic can be supplemented with open source ML resources such as python's dedupe.

First, I created a script that leverages pydbgen to randomly generate records with data quality issues that one might observe in a
MDM system (NULLs, typographical errors, etc.). The goal with these records was to create multiple records that in reality correspond
to the same entity and to see if it would be possible that despite the data quality issues one can identify groupings of records that
correspond to the same entity.

Second, I leveraged python's dedupe to train a classification model as well as a clustering model on this task, ultimately achieving
majority cluster identification of 71%.
