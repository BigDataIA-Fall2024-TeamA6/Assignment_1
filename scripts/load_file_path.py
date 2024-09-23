import boto3
import mysql.connector
import os

# S3 and MySQL configuration
BUCKET_NAME = 'bdia-assignment-1'
S3_PREFIX = 'ValidationData/'  # Folder path in the bucket
S3_BASE_URL = f"https://{BUCKET_NAME}.s3.amazonaws.com/{S3_PREFIX}"  # Base URL format for S3 objects

MYSQL_HOST = 'database-1.cdwumcckkqqt.us-east-1.rds.amazonaws.com'
MYSQL_USER = 'admin'
MYSQL_PASSWORD = 'amazonrds7245'
MYSQL_DATABASE = 'gaia_benchmark_dataset_validation'
MYSQL_TABLE = 'validation_table'

# Connect to MySQL RDS
def connect_to_mysql():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

# Function to update file_path in the MySQL table
def update_file_path(task_id, file_path):
    try:
        conn = connect_to_mysql()
        cursor = conn.cursor()
        
        # Update query for the file_path
        update_query = f"UPDATE {MYSQL_TABLE} SET file_path = %s WHERE task_id = %s"
        cursor.execute(update_query, (file_path, task_id))
        conn.commit()

        print(f"Updated file_path for task_id {task_id}: {file_path}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Function to retrieve S3 objects and update the RDS table
def update_rds_with_s3_paths():
    s3 = boto3.client('s3', region_name='us-east-1')

    # List objects in the S3 bucket under the specified prefix
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=S3_PREFIX)

    if 'Contents' not in response:
        print(f"No files found in {S3_PREFIX}")
        return

    # Iterate over the objects in the S3 bucket
    for obj in response['Contents']:
        s3_key = obj['Key']
        file_name = os.path.basename(s3_key)
        task_id, file_extension = os.path.splitext(file_name)  # task_id is filename without extension

        if task_id:
            # Build the full S3 object URL
            s3_file_url = f"{S3_BASE_URL}{file_name}"

            # Update the file_path in RDS table
            update_file_path(task_id, s3_file_url)

if __name__ == "__main__":
    update_rds_with_s3_paths()
