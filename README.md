Document Clustering with Python
================

<img src='header_short.jpg'>

This repo is for clustering and analysing search results for diseases in the publications from the "pubmed" database. 
You can learn more about PubMed resources at:

Currently, uses json output for the the articles. These files contain sourceid, sourcedb,text and denotations of the search records returned. They only return Mesh ids of denotations and not the corresponding text. This is a big handicap and needs to be resolved.

The <b>labeled set</b> clustering using K-means++ shows accuracy > 90% without using the labels in the process of clustering
The label names were semi-self generated from Mesh ids in the XML document and can easily be automated
Data analysis showed an elbow at n=6 as was expected from the labels
The labels in training set used for accuracy calculation

The <b>unlabeled set</b> showed an elbow at n=8 but on analysis it was found that 
For Future
----------
<ul>
<li> Use disease name from bioc(xml) outputs instead of disease ids for labeling.
<li> Create and use a map of acronyms to their full forms using the Mesh description in the xml files
<li> Exploring ngram collocations >1 to use with the vectorizer</li>
<li> Explore other clustering techniques</li>
<li> Identify and use knowlege bases and synsets to use</li>
</ul>



### Repository

To analyze the textual document open the LabeledSetAnalysis.ipynb and UnlabeledSetAnalysis.ipynb notepad in jupyter notebook.

To perform the actual clustering run "clustering.py" 

usage:
	python clustering.py | [outputfile]
	Where:
	<b>outputfile:</b> the file that will store the result

	Example:
	python clustering.py > result.out

Pregenerated results are in "result.txt" 

PMID list data and the search results are in the "Data" folder

