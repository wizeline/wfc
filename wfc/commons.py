import os

__home__ = os.path.abspath(os.path.dirname(__file__))


def asset_path(asset: str) -> str:
    return os.path.join(__home__, 'assets', asset)


def get_boolean_environ(variable_name):
    return False if os.environ.get(variable_name) in ('', None) else True
