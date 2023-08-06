from optel.datalake import ingest

import pytest


@pytest.mark.skip(reason="Not working on runner, cant set SPARK_HOME")
def test_write_to_elastic(me_df_timestamp):
    destination = 'test-datalake'
    username = 'elastic-bot-write'
    password = 'M2cscea.Istt'
    nodes = 'https://6f3b94ab79c327269a56379a235bdf86.us-central1.gcp.cloud.es.io:9243'
    ingest.write_to_elastic(
        me_df_timestamp, destination, nodes, username, password)
