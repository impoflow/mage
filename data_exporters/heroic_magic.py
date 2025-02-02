from mage_ai.orchestration.triggers.api import trigger_pipeline
if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def trigger(*args, **kwargs):
    """
    Trigger another pipeline to run.

    Documentation: https://docs.mage.ai/orchestration/triggers/trigger-pipeline
    """

    trigger_pipeline(
        'pipeline_uuid',        
        variables={},           
        check_status=False,
        error_on_failure=False,
        poll_interval=60,
        poll_timeout=None,
        verbose=True,
    )
