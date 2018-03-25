import os

MONGODB = {
    'username': os.environ.get('MONGODB_USERNAME','username'),
    'password': os.environ.get('MONGODB_PASSWORD','password'),
    'host': os.environ.get('mongo_host','127.0.0.1'),
    'port': os.environ.get('mongo_port','27017'),
    'db': os.environ.get('MONGODB_DBNAME','db_name')
}

AWS_BUCKET = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_ACCESS_KEY_ID = ''
