import asyncio
import motor
from tornado import web, gen, ioloop, escape, platform

from db import MongoWrapper
from utils import get_sha256, AWSWrapper

class UploadHandler(web.RequestHandler):
    def check_origin(self, origin):
        return True

    async def get(self, token):
        db_client = MongoWrapper()
        file = await db_client.get_file_by_id(token)
        if not file:
            self.clear()
            self.set_status(404)
            resp = {'Error': "Error file key"}
            self.finish(escape.json_encode(resp))
        else:
            aws_client = AWSWrapper(key=token, file_name=file['file_name'], loop=loop)
            file_content = await aws_client.get_file()
            file_name = file['file_name']
            resp = {'file_name': str(file_name), 'file_content': str(file_content)}
            self.write(escape.json_encode(resp))

    async def put(self, token):
        file = self.request.files['file'][0]
        file_name = file['filename']
        file_content = file['body']
        hash_str = get_sha256(file_content)
        db_client = MongoWrapper()
        file_doc = await db_client.get_file_by_name_and_hash(file_name, hash_str)
        if file_doc:
            key = str(file_doc['_id'])
        else:
            key = await db_client.insert_file(file_name, hash_str)
            print(key)
            aws_client = AWSWrapper(key=key, file_name=file_name, loop=loop)
            await aws_client.upload_file(file_content)
        resp = {'key': key}
        self.write(escape.json_encode(resp))


if __name__ == '__main__':
    app = web.Application([
        (r'/([^/]+)', UploadHandler),
    ])
    app.listen(8888)
    # loop = ioloop.IOLoop.instance()
    # loop.start()
    platform.asyncio.AsyncIOMainLoop().install()
    app.listen(8080)
    loop = asyncio.get_event_loop()
    loop.run_forever()