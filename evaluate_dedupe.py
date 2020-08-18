import pandas as pd

def add_majority(clusters_fp):
    data_w_clusters = pd.read_csv(clusters_fp)
    both_ids = pd.read_csv('xref_eval_clusters.csv')

    data_w_clusters['eip_id'] = both_ids['eip_id']
    data_w_clusters['xref_id'] = both_ids['xref_id']

    # identify the majority cluster
    eip_id_maj_cluster_mapping = data_w_clusters[['eip_id','Cluster ID']].groupby('eip_id').agg(lambda x:x.value_counts().index[0]).to_dict()
    data_w_clusters['majority_cluster'] = data_w_clusters['eip_id'].apply(lambda x: eip_id_maj_cluster_mapping['Cluster ID'][x])
    data_w_clusters['Correct'] = data_w_clusters['Cluster ID']==data_w_clusters['majority_cluster']
    return data_w_clusters

def eval_summary(df):
    print("Correctly identified majority cluster: " + str(df['Correct'].describe()['freq'])+"/"+str(df['Correct'].describe()['count'])+ " or " + str(round(100.0*round(df['Correct'].describe()['freq']/df['Correct'].describe()['count'],2)))+ " percent of the time")

if __name__=='__main__':
    output_w_majorities = add_majority('xref_clustering.csv')

    eval_summary(output_w_majorities)