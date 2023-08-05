"""
Set of function related to handling the configuration of this option.
"""
from pkglts.dependency import Dependency


def require(purpose, cfg):
    """List of requirements for this option for a given purpose.

    Args:
        purpose (str): either 'option', 'setup', 'install' or 'dvlpt'
        cfg (Config):  current package configuration

    Returns:
        (list of Dependency)
    """
    del cfg

    if purpose == 'option':
        options = ['pysetup']
        return [Dependency(name) for name in options]

    return []
