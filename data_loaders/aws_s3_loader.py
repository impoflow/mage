import boto3

import base64
from io import BytesIO
import os

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_from_s3_bucket(*args, **kwargs):
    bucket_name = kwargs['bucket_name']
    user = kwargs['user']
    project = kwargs['project_name']

    s3 = boto3.client('s3')

    obj = s3.get_object(Bucket=bucket_name, Key=user + '/' + project + '.zip')
    zip_bytes = obj['Body'].read()
    
    zipfile_in_memory = BytesIO(zip_bytes)
    
    serialized_zip = {
        'filename': project,
        'content': base64.b64encode(zipfile_in_memory.getvalue()).decode('utf-8'),
        'size': zipfile_in_memory.getbuffer().nbytes
    }

    return serialized_zip

@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'