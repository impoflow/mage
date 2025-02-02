import base64
from io import BytesIO

class S3DataLoader:
    def __init__(self, s3_client):
        self.s3_client = s3_client
    
    def load(self):
        pass

class S3ZipLoader(S3DataLoader):
    def __init__(self, s3_client):
        super().__init__(s3_client)

    def load(self, bucket_name, user, project_name):
        obj = self.s3_client.get_object(Bucket=bucket_name, Key=user + '/' + project_name + '.zip')
        zip_bytes = obj['Body'].read()

        zipfile_in_memory = BytesIO(zip_bytes)

        serialized_zip = {
            'filename': project_name,
            'content': base64.b64encode(zipfile_in_memory.getvalue()).decode('utf-8'),
            'size': zipfile_in_memory.getbuffer().nbytes
        }

        return serialized_zip