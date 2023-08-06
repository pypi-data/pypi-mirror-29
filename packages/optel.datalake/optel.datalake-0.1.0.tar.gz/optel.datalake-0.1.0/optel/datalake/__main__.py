import sys


if __name__ == '__main__' and not __package__:
    # This should never happen when installed from pip (setup.py).
    # This workaround is NOT bulletproof, rather brittle as many edge
    # cases are not covered
    # See http://stackoverflow.com/a/28154841/2479038
    print('warning: running package directly, risking ImportError',
          file=sys.stderr)


from optel.datalake import __project__  # noqa
from optel.datalake.cli import main  # noqa


if __name__ == '__main__':
    sys.exit(main(prog_name=__project__))
