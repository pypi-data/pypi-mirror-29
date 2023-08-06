from flake8.formatting import base


class JunitFormatter(base.BaseFormatter):
    """JUnit formatter for Flake8."""

    def format(self, error):
        return 'Example formatter: {0!r}'.format(error)
