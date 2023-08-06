import click
import logging


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
def boot():
    pass


@cluster.command()
def kill():
    pass


if __name__ == '__main__':
    main(progname=__project__)
