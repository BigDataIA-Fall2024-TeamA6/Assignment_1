import boto3
from huggingface_hub import HfApi, hf_hub_download
import os

# Initialize S3 client
s3_client = boto3.client('s3', region_name = 'us-east-1')

# Define constants
HUGGINGFACE_REPO_ID = "gaia-benchmark/GAIA"  # Base repo ID for the dataset
SUBFOLDER = "2023/validation"  # Subfolder for the specific files
S3_BUCKET_NAME = "bdia-assignment-1"
S3_VALIDATION_PREFIX = "ValidationData/"
METADATA_FILE_NAME = "metadata.jsonl"
HUGGINGFACE_TOKEN = "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"  # Replace with your Hugging Face token

# Hugging Face API instance with token
api = HfApi()

def upload_to_s3(file_path, s3_bucket, s3_key):
    """Upload file content to S3."""
    try:
        with open(file_path, 'rb') as f:
            s3_client.upload_fileobj(f, s3_bucket, s3_key)
        print(f"Successfully uploaded {s3_key} to s3://{s3_bucket}/{s3_key}")
    except Exception as e:
        print(f"Failed to upload {s3_key} to S3: {str(e)}")

def main():
    # List files in the repository, specifying repo_type as 'dataset'
    repo_files = api.list_repo_files(HUGGINGFACE_REPO_ID, repo_type="dataset")

    # Filter files to those in the subfolder ('2023/validation')
    subfolder_files = [f for f in repo_files if f.startswith(SUBFOLDER)]

    # Download and move each file to S3
    for file_name in subfolder_files:
        # Download each file from Hugging Face Hub (use subfolder path in filename)
        local_file_path = hf_hub_download(repo_id=HUGGINGFACE_REPO_ID, filename=file_name, repo_type="dataset", use_auth_token=HUGGINGFACE_TOKEN)
        
        # Define the S3 key (path in S3 bucket)
        if file_name.endswith(METADATA_FILE_NAME):
            s3_key = METADATA_FILE_NAME  # Place metadata.jsonl in the root
        else:
            s3_key = f"{S3_VALIDATION_PREFIX}{file_name.split('/')[-1]}"  # Place other files in ValidationData/

        # Upload the file to S3
        upload_to_s3(local_file_path, S3_BUCKET_NAME, s3_key)

        # Remove the local file after uploading
        os.remove(local_file_path)

if __name__ == "__main__":
    main()
