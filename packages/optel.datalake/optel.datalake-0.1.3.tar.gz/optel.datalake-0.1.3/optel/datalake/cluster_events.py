import googleapiclient.discovery
import subprocess


def boot_cluster(instances_names, project, zone):
    """
    Boot a dataproc cluster on GC.

    Args:
        instances_names (list): A list of instances to boot.
        project (str): The project where to boot instances.
        zone (str): The zone of the project.

    Example:
        compute.instances().start(project=project, instance=instance[0],
        zone=zone.)
    """
    compute = googleapiclient.discovery.build('compute', 'v1')

    print("Booting", instances_names)
    for instance in instances_names:
        compute.instances().start(
            project=project, zone=zone, instance=instance).execute()


def shutdown_cluster(instances_names, project, zone, cluster):
    """
    Shutdown a dataproc cluster if no jobs are running.

    Args:
        instances_names (list): A list instances to shutdown.
        project (str): The project where to boot instances.
        zone (str): The zone of the project.
        cluster (str): The cluster to shutdown
    """
    compute = googleapiclient.discovery.build('compute', 'v1')

    print("Checking if a job is running")
    status = subprocess.check_output(["gcloud", "dataproc", "jobs", "list",
                                      "--cluster", cluster,
                                      "--region", zone[:-2],
                                      "--state-filter", "active"])
    print(status)
    if b"JOB_ID" in status:
        print("Job running, not shutting down the cluster")

    else:
        print("No jobs running, shutting down cluster")
        for instance in instances_names:
            compute.instances().stop(
                project=project, zone=zone, instance=instance).execute()


def get_instances_names(project, zone, cluster):
    """
    Get instance names based on cluster name and their status.

    Args:
        project (str): The project where to get the names.
        zone (str): The zone of the project.
        cluster (str): The cluster to get the instances names.

    Returns:
        list: Selected instances based on cluster.

    """
    compute = googleapiclient.discovery.build('compute', 'v1')

    project_objects = compute.instances().list(
        project=project, zone=zone).execute()

    cluster_status = compute.instances().get(
        project=project, zone=zone,
        instance=project_objects['items'][0]['name']).execute()['status']
    instances_names = []
    ninstances = len(project_objects['items'])
    for instance in range(ninstances):
        instances_names.append(project_objects['items'][instance]['name'])
    selected_instances = []
    for instance in instances_names:
        if cluster in instance:
            selected_instances.append(instance)
    return selected_instances, cluster_status
