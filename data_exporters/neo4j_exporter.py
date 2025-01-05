from os import path

from pandas import DataFrame

from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader

from mage.utils.db_connection import Neo4jConnection
from mage.utils.db_handler import Neo4jHandler
import neo4j

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

@data_exporter
def export_data(df: DataFrame, **kwargs):
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
    
    config_loader = ConfigFileLoader(config_path, config_profile)
    neo4j_config = config_loader.config

    uri = neo4j_config.get('NEO_CONNECTION_STRING')
    user = neo4j_config.get('NEO_USER')
    password = neo4j_config.get('NEO_PASSWORD')

    neo4j_connection = Neo4jConnection(uri, user, password)
    neo4j_connection.connect()

    handler = Neo4jHandler(neo4j_connection)

    try:
        handler.add_user(kwargs['user'])
        handler.add_project(kwargs['project_name'], kwargs['user'])
        handler.add_classes_from_csv(kwargs['user'], kwargs['project_name'], df)
        handler.create_ownership(kwargs['user'], kwargs['project_name'])

        for user in kwargs['collaborators']:
            handler.add_user(user)
            handler.create_collab(user, kwargs['project_name'], kwargs['user'])
        
    finally:
        neo4j_connection.close()