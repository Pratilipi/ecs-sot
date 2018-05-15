import os

# no. of parallel threads
NO_OF_READ_THREADS = 10
NO_OF_PROCESS_THREADS = 10

# sqs 
AWS_REGION = 'ap-south-1'
SQS_NAME = 'devo-ecs-sot'

"""
# db settings
DB_PAGE_SIZE = 1000
DB = {'name': 'author',
      'host': os.environ['MASTER_DB_ENDPOINT_RO'],
      'port': 3306,
      'user': 'root' if 'MASTER_MYSQL_DB_USERNAME' not in os.environ else os.environ['MASTER_MYSQL_DB_USERNAME'],
      'pass': 'root' if 'MASTER_MYSQL_DB_PASSWORD' not in os.environ else os.environ['MASTER_MYSQL_DB_PASSWORD'] }
"""
