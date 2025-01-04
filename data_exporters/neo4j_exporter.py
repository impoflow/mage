if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

import pandas as pd
from mage.utils.db_connection import Neo4jConnection
from mage.utils.db_handler import Neo4jHandler
import neo4j
import os

from mage_ai.data_preparation.shared.secrets import get_secret_value


@data_exporter
def export_data(data, *args, **kwargs):
    # in local set uri as host.dokcer.internal
    uri = f"bolt://{get_secret_value('neo4j_uri')}:7687"
    user = get_secret_value('neo4j_user')
    password = get_secret_value('neo4j_password')

    neo4j_connection = Neo4jConnection(uri, user, password)
    neo4j_connection.connect()

    handler = Neo4jHandler(neo4j_connection)

    try:
        handler.add_user(kwargs['user'])
        handler.add_project(kwargs['project_name'], kwargs['user'])
        handler.add_classes_from_csv(kwargs['user'], kwargs['project_name'], data)
        handler.create_ownership(kwargs['user'], kwargs['project_name'])

        for user in kwargs['collaborators']:
            handler.add_user(user)
            handler.create_collab(user, kwargs['project_name'], kwargs['user'])
        
    finally:
        neo4j_connection.close()