import pandas as pd
import boto3

from mage.utils.s3 import S3ZipLoader

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def load(*args, **kwargs):

    s3_client = boto3.client('s3')

    loader = S3ZipLoader(s3_client)
    
    data = loader.load(
        kwargs['bucket_name'],
        kwargs['user'],
        kwargs['project_name']
    )

    return data

@test
def test_is_dataframe(output, *args) -> None:
    assert isinstance(output, dict), f'Expected output to be a DataFrame, but got {type(output)}'

@test
def test_output_not_none(output, *args) -> None:
    assert output is not None, 'The output is undefined'

@test
def test_output_not_empty(output, *args) -> None:   
    assert len(output) > 0, 'The output DataFrame is empty'