'''
Created on Dec 6, 2017

@author: khiem
'''
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS']='/home/khiem/workspace/INABachPhuBTSAnalytics-fa0fa8698768.json'

# Imports the Google Cloud client library
from google.cloud import bigquery

# Instantiates a client
bigquery_client = bigquery.Client()

# The name for the new dataset
dataset_id = 'my_new_dataset'

# Prepares a reference to the new dataset
dataset_ref = bigquery_client.dataset(dataset_id)
dataset = bigquery.Dataset(dataset_ref)

# Creates the new dataset
# dataset = bigquery_client.create_dataset(dataset)
# bigquery_client.delete_dataset(dataset)

# print('Dataset {} created.'.format(dataset.dataset_id))

# Query
query_job = bigquery_client.query("""
    #standardSQL
    SELECT corpus AS title, COUNT(*) AS unique_words
    FROM `bigquery-public-data.samples.shakespeare`
    GROUP BY title
    ORDER BY unique_words DESC
    LIMIT 10""")

results = query_job.result()  # Waits for job to complete.
print results
for row in results:
    print row
    print("{}: {}".format(row.title, row.unique_words))
    
    
    
    