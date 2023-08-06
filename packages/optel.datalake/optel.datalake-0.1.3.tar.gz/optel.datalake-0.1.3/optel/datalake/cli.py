import click
import logging
from optel.datalake import cluster_events
from optel.datalake import __version__, __project__


@click.group()
@click.version_option(__version__)
def main():
    logging.basicConfig(filename='info.log',
                        level=logging.INFO,
                        filemode='w')


@main.group()
def cluster():
    pass


@cluster.command()
@click.option('--project', help='Project where the instances are')
@click.option('--zone', help='Zone where the project exist')
@click.option('--cluster', help='Cluster to boot')
def boot(project, zone, cluster):
    instances = cluster_events.get_instances_names(project, zone, cluster)[0]
    cluster_events.boot_cluster(instances, project, zone)


@cluster.command()
@click.option('--project', help='Project where the instances are')
@click.option('--zone', help='Zone where the project exist')
@click.option('--cluster', help='Cluster to kill')
def kill(project, zone, cluster):
    instances = cluster_events.get_instances_names(project, zone, cluster)[0]
    cluster_events.shutdown_cluster(instances, project, zone, cluster)


if __name__ == '__main__':
    main(progname=__project__)
