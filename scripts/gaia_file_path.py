import pandas as pd
import boto3
import io
import os

# Set up your S3 bucket details and base URL for file paths
s3_bucket_name = 'bdia-assignment-1'
metadata_file_key = 'MetaDataTSV.tsv'
validation_folder = 'ValidationData/'
base_s3_url = 'https://bdia-assignment-1.s3.amazonaws.com/ValidationData/'

# Initialize boto3 S3 client
s3 = boto3.client('s3', region_name='us-east-1')  # Adjust the region if necessary

# Function to read a TSV file from S3 into a pandas DataFrame
def read_tsv_from_s3(bucket_name, key):
    obj = s3.get_object(Bucket=bucket_name, Key=key)
    tsv_data = obj['Body'].read().decode('utf-8')
    df = pd.read_csv(io.StringIO(tsv_data), sep='\t')
    return df

# Load MetaDataTSV.tsv from S3
metadata_df = read_tsv_from_s3(s3_bucket_name, metadata_file_key)

# Initialize a list to store task_id and file_path
output_data = []

# List all files in the ValidationData/ folder in the S3 bucket
response = s3.list_objects_v2(Bucket=s3_bucket_name, Prefix=validation_folder)

for obj in response.get('Contents', []):
    file_name = os.path.basename(obj['Key'])  # Extract file name

    # Check if the file exists in the MetaDataTSV.tsv file
    matching_row = metadata_df[metadata_df['file_name'] == file_name]
    if not matching_row.empty:
        task_id = matching_row['task_id'].values[0]
        # Construct the full file path
        file_path = f'{base_s3_url}{file_name}'
        output_data.append({'task_id': task_id, 'file_path': file_path})

# Create a DataFrame for the output data
output_df = pd.DataFrame(output_data)

# Convert the DataFrame to a TSV format in-memory
tsv_buffer = io.StringIO()
output_df.to_csv(tsv_buffer, sep='\t', index=False)

# Upload the TSV file back to the S3 bucket
output_file_key = 'gaia_file_path.tsv'
s3.put_object(Bucket=s3_bucket_name, Key=output_file_key, Body=tsv_buffer.getvalue())

print(f'Output file with paths saved to s3://{s3_bucket_name}/{output_file_key}')