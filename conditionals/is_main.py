if 'condition' not in globals():
    from mage_ai.data_preparation.decorators import condition


@condition
def evaluate_condition(data, *args, **kwargs) -> bool:
    if 'is_main' in data.columns and data['is_main'].sum() == 1:
        return True
    else:
        return False