import mysql.connector

class DBConnection:
    _instance = None
    
    def __init__(self):
        if not DBConnection._instance:
            DBConnection._instance = self

            # Connect to Amazon RDS Database
            self.connection = mysql.connector.connect(
            host='database-1.cdwumcckkqqt.us-east-1.rds.amazonaws.com',
            user='admin',
            password='amazonrds7245',
            database='gaia_benchmark_dataset_validation')
            self.cursor = self.connection.cursor()

            print("Connected to DB")
        else:
            raise Exception("This class is a singleton!")
    
    @staticmethod
    def get_instance():
        if not DBConnection._instance:
            DBConnection()
        return DBConnection._instance
