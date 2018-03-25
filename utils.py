import hashlib

import aiobotocore

import settings


def get_sha256(source):
    m = hashlib.sha256()
    m.update(source)
    return m.hexdigest()


class AWSWrapper:
    def __init__(self, key, loop, file_name):
        self.session = aiobotocore.get_session()
        self.key = '{}/{}'.format(key, file_name)

    async def upload_file(self, file_content):
        async with self.session.create_client('s3', region_name='eu-west-3',
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID) as client:
            resp = await client.put_object(Bucket=settings.AWS_BUCKET,
                                            Key=self.key,
                                            Body=file_content)
            return resp

    async def get_file(self):
        async with self.session.create_client('s3', region_name='eu-west-3',
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID) as client:
            response = await client.get_object(Bucket=settings.AWS_BUCKET, Key=self.key)
            async with response['Body'] as stream:
                data = await stream.read()
            return data
