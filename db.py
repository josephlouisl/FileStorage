from bson.objectid import ObjectId
from bson.errors import InvalidId
import urllib

import motor.motor_tornado

import settings

class MongoWrapper():
    def __init__(self):
        username = username = urllib.parse.quote_plus(settings.MONGODB['username'])
        password = urllib.parse.quote_plus(settings.MONGODB['password'])
        mongo_host = settings.MONGODB['host']
        mongo_port = settings.MONGODB['port']
        db_name = settings.MONGODB['db']
        mongo_client = motor.motor_tornado.MotorClient('mongodb://%s:%s@%s:%s' % (username, password, mongo_host, mongo_port))
        self.db = mongo_client.db_name

    async def get_file_by_id(self, id):
        files = self.db.files
        try:
            file = await files.find_one({'_id': ObjectId(id)})
            return file
        except InvalidId:
        	return False

    async def get_file_by_name_and_hash(self, file_name, hash_str):
        files = self.db.files
        file = await files.find_one({'file_name': file_name, 'hash': hash_str})
        return file

    async def get_file_by_hash(self, hash_str):
        files = self.db.files
        file = await files.find_one({'hash': hash_str})
        return file

    async def insert_file(self, file_name, hash_str):
        files = self.db.files
        file = {
            'hash': hash_str,
            'file_name': file_name,
        }
        file = await files.insert_one(file)
        return str(file.inserted_id)
