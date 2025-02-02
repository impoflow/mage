import pandas as pd

from mage.utils.transformer import DataTransformer

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    transformer = DataTransformer()
    transformed_data = transformer.transform(data)
    print(transformed_data)
    return transformed_data

@test
def test_is_dataframe(output, *args) -> None:
    assert isinstance(output, pd.DataFrame), f'Expected output to be a DataFrame, but got {type(output)}'

@test
def test_output_not_none(output, *args) -> None:
    assert output is not None, 'The output is undefined'

@test
def test_output_not_empty(output, *args) -> None:   
    assert not output.empty, 'The output DataFrame is empty'