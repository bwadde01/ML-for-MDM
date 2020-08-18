import dedupe
import pandas as pd
import json
import csv
import os
from ast import literal_eval


# def format_records(filepath,index_col=index):
#     df = pd.read_csv(filepath)
#     df.fillna("None",inplace=True)
#     return df.to_json(orient='index')

def readData(filename):
    """
    Read in our data from a CSV file and create a dictionary of records, 
    where the key is a unique record ID and each value is dict

    Make sure each blank is populated as 'None'
    """

    data_d = {}
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            row_id = int(row['xref_id'])
            data_d[row_id] = dict(row.items())

    return data_d

def create_training_from_csv(fp):
    df = pd.read_csv(fp)
    df.set_index('eip_id',inplace=True)
    distinct = []
    match = []
    for id1,row1 in df.iterrows():
        for id2,row2 in df.iterrows():
            if row1['xref_id']!=row2['xref_id']:
                if id1==id2:
                    match.append([literal_eval(row1.to_json()),literal_eval(row2.to_json())])
                else:
                    distinct.append([literal_eval(row1.to_json()),literal_eval(row2.to_json())])
            else:
                continue
    training_content = {"distinct":distinct,"match":match}
    print(training_content)
    # print(training_content['match'])
    # now write to file
    with open('training_file.json','w') as write_file:
        json.dump(training_content,write_file)
    return

def variable_defs(data_config):
    return [{'field':col,'type':typ,'has missing':True} for col,typ in data_config.items()]

if __name__=='__main__':

    # generate variable definitions input to dedupe object
    with open('data_model_config.json',) as f:
        dm_config = json.load(f)
    f.close()
    variable_definitions = variable_defs(dm_config)

    dd = dedupe.Dedupe(variable_definitions) 

    # upload and preprocess data
    print("Reading in Data")
    xref = readData('xref_all_data.csv')
    

    print("Preparing for Training")
    if os.path.exists('training_file.json'):
        print('reading labeled examples from training_file.json')
        with open('training_file.json', 'rb') as f:
            dd.prepare_training(xref, f)
    else:
        print("Creating Training File")    
        create_training_from_csv('xref_training_data_sample.csv')
        print('reading labeled examples from training_file.json')
        with open('training_file.json', 'rb') as f:
            dd.prepare_training(xref, f)

    print("Commencing Training")
    dd.train(index_predicates=False)

    print("Partitioning")
    clustered_dupes = dd.partition(xref,threshold=0.5)

    print("Writing Clusters to Data")
    cluster_membership = {}
    for cluster_id, (records, scores) in enumerate(clustered_dupes):
        for record_id, score in zip(records, scores):
            cluster_membership[record_id] = {
                "Cluster ID": cluster_id,
                "confidence_score": score
            }

    with open('xref_clustering.csv', 'w') as f_output, open('xref_all_data.csv') as f_input:

        reader = csv.DictReader(f_input)
        fieldnames = ['Cluster ID', 'confidence_score'] + reader.fieldnames

        writer = csv.DictWriter(f_output, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            row_id = int(row['xref_id'])
            row.update(cluster_membership[row_id])
            writer.writerow(row)
