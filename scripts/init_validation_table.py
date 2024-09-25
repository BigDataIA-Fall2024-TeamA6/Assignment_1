import os
import json
import numpy as np
import pandas as pd
import mysql.connector
from huggingface_hub import login
from datasets import load_dataset
from sqlalchemy import create_engine


# Connect to Amazon RDS Database
connection = mysql.connector.connect(
            host='database-1.cdwumcckkqqt.us-east-1.rds.amazonaws.com',
            user='admin',
            password='amazonrds7245',
            database='gaia_benchmark_dataset_validation',
            allow_local_infile=True )
            

 
#Hugging face login and authentication
HF_TOKEN = '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'

os.environ['HF_TOKEN'] = HF_TOKEN
login(token=HF_TOKEN)


#Load Dataset
gaia_dataset = load_dataset("gaia-benchmark/GAIA", "2023_all", split='validation')

gaia_df = pd.DataFrame(gaia_dataset)


# Select the necessary columns and clean the data
gaia_df.columns = gaia_df.columns.str.lower().str.replace(' ', '_')
validation_table = gaia_df[['task_id','question','final_answer','file_name','file_path','annotator_metadata']]
validation_table['validation_status'] = np.zeros(165,dtype=int)
validation_table['serial_no'] = np.arange(1,166)
validation_table = validation_table[['serial_no','task_id', 'question', 'final_answer', 'file_name', 'file_path',
       'annotator_metadata', 'validation_status']]
validation_table['annotator_metadata'] = validation_table['annotator_metadata'].apply(lambda x : x["Steps"].split("\n"))
validation_table['annotator_metadata'] = validation_table['annotator_metadata'].apply(lambda x : json.dumps(x))


engine = create_engine("mysql+mysqlconnector://admin:amazonrds7245@database-1.cdwumcckkqqt.us-east-1.rds.amazonaws.com/gaia_benchmark_dataset_validation")

validation_table.to_sql(con = engine, name='validation_table',if_exists='replace')
