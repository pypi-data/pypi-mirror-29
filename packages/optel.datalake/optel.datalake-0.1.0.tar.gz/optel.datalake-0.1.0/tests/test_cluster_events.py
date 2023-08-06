from optel.datalake import cluster_events
# import pytest

project = "optel-data-lab"
zone = "us-east1-d"
cluster = "cluster-datalab-01"


# @pytest.mark.skip(reason="Needs GC credentials to test this.")
def test_get_instances_names(gc_instances):
    instances = cluster_events.get_instances_names(project, zone, cluster)
    print(instances[1])
    assert "runner" not in instances
    assert instances[1] != ""


# @pytest.mark.skip(reason="Needs GC credentials to test this.")
def test_boot_cluster(instances_names):
    cluster_events.boot_cluster(instances_names, project, zone)


def test_shutdown_cluster(instances_names):
    cluster_events.shutdown_cluster(instances_names, project, zone, cluster)
