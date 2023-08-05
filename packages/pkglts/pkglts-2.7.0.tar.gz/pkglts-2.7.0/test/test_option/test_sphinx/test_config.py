from pkglts.config_management import Config
from pkglts.option.sphinx.config import check, require, update_parameters


def test_update_parameters():
    cfg = {}
    update_parameters(cfg)
    assert len(cfg['sphinx']) == 3


def test_config_check_sphinx_theme():
    for theme in (1, None,):
        cfg = Config(dict(doc={'fmt': 'rst'}, sphinx={'theme': theme}))
        assert 'sphinx.theme' in check(cfg)


def test_require():
    cfg = Config(dict(sphinx={'theme': "default"}))

    assert len(require('option', cfg)) == 3
    assert len(require('setup', cfg)) == 0
    assert len(require('install', cfg)) == 0
    assert len(require('dvlpt', cfg)) == 1
