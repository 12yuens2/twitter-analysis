# Digifest 2016 Twitter analysis

## Requirements
Please make sure you have these libraries installed before running the notebook.

* matplotlib	v. 1.3.1
* networkx 	v. 1.11
* numpy		v. 1.8.2
* pandas	v. 0.18.0
* pygraphviz 	v. 1.3.1
* wordcloud 	v. 1.2.1

A full list of requirements that the notebook runs under can be found in the 
file `requirements.txt` so use the command

`pip install -r requirements.txt` 

if the notebook still has issues with not finding modules.

## Running the notebook
The notebook titled `Digifest-2016-Twitter-analysis.ipynb` is the notebook with 
our code, graphics and analysis of the twitter dataset. 

It uses the following python files and images, so please make sure they are in 
the same directory before running the notebook.

* re_function.py
* hashtag_plot.py
* word_cloud.py
* logo.png


## Use of json-csv-converter.py
Set up the script permissions for use with:

`chmod 755 json-csv-converter.py`

Run the script with

`./json-csv-converter.py [TWITTER JSON FILE] [NAME FOR CSV FILE]`

A csv version of the json file will be written to a file of the specified name.
The csv file will have the same fields as digifest2016dataset.csv.


## Images
The directory imgs stores the backup images in case the python notebook does not generate the networkx graphs. 

