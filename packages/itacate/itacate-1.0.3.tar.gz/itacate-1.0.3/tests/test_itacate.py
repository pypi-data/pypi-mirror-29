# -*- coding: utf-8 -*-
"""
    tests.test_config
    ~~~~~~~~~~~~~~~~~

    :copyright: © 2010 by the Pallets team.
    :license: BSD, see LICENSE for more details.
"""

from datetime import timedelta
import os

import itacate
import pytest


# config keys used for the TestConfig
TEST_KEY = 'foo'
SECRET_KEY = 'config'


def common_object_test(config):
    assert config['TEST_KEY'] == 'foo'
    assert 'TestConfig' not in config


def test_config_from_file():
    config = itacate.Config(__name__)
    config.from_pyfile(__file__.rsplit('.', 1)[0] + '.py')
    common_object_test(config)


def test_config_from_object():
    config = itacate.Config(__name__)
    config.from_object(__name__)
    common_object_test(config)


def test_config_from_json():
    config = itacate.Config(__name__)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config.from_json(os.path.join(current_dir, 'static', 'config.json'))
    common_object_test(config)


def test_config_from_mapping():
    config = itacate.Config(__name__)
    config.from_mapping({
        'SECRET_KEY': 'config',
        'TEST_KEY': 'foo'
    })
    common_object_test(config)

    config = itacate.Config(__name__)
    config.from_mapping([
        ('SECRET_KEY', 'config'),
        ('TEST_KEY', 'foo')
    ])
    common_object_test(config)

    config = itacate.Config(__name__)
    config.from_mapping(
        SECRET_KEY='config',
        TEST_KEY='foo'
    )
    common_object_test(config)

    config = itacate.Config(__name__)
    with pytest.raises(TypeError):
        config.from_mapping(
            {}, {}
        )


def test_config_from_class():
    class Base(object):
        TEST_KEY = 'foo'

    class Test(Base):
        SECRET_KEY = 'config'

    config = itacate.Config(__name__)
    config.from_object(Test)
    common_object_test(config)


def test_config_from_envvar():
    env = os.environ
    try:
        os.environ = {}
        config = itacate.Config(__name__)
        with pytest.raises(RuntimeError) as e:
            config.from_envvar('FOO_SETTINGS')
        assert "'FOO_SETTINGS' is not set" in str(e.value)
        assert not config.from_envvar('FOO_SETTINGS', silent=True)

        os.environ = {'FOO_SETTINGS': __file__.rsplit('.', 1)[0] + '.py'}
        assert config.from_envvar('FOO_SETTINGS')
        common_object_test(config)
    finally:
        os.environ = env


def test_config_from_envvar_missing():
    env = os.environ
    try:
        os.environ = {'FOO_SETTINGS': 'missing.cfg'}
        with pytest.raises(IOError) as e:
            config = itacate.Config(__name__)
            config.from_envvar('FOO_SETTINGS')
        msg = str(e.value)
        assert msg.startswith('[Errno 2] Unable to load configuration '
                              'file (No such file or directory):')
        assert msg.endswith("missing.cfg'")
        assert not config.from_envvar('FOO_SETTINGS', silent=True)
    finally:
        os.environ = env


def test_config_missing():
    config = itacate.Config(__name__)
    with pytest.raises(IOError) as e:
        config.from_pyfile('missing.cfg')
    msg = str(e.value)
    assert msg.startswith('[Errno 2] Unable to load configuration '
                          'file (No such file or directory):')
    assert msg.endswith("missing.cfg'")
    assert not config.from_pyfile('missing.cfg', silent=True)


def test_config_missing_json():
    config = itacate.Config(__name__)
    with pytest.raises(IOError) as e:
        config.from_json('missing.json')
    msg = str(e.value)
    assert msg.startswith('[Errno 2] Unable to load configuration '
                          'file (No such file or directory):')
    assert msg.endswith("missing.json'")
    assert not config.from_json('missing.json', silent=True)


def test_get_namespace():
    config = itacate.Config(__name__)
    config['FOO_OPTION_1'] = 'foo option 1'
    config['FOO_OPTION_2'] = 'foo option 2'
    config['BAR_STUFF_1'] = 'bar stuff 1'
    config['BAR_STUFF_2'] = 'bar stuff 2'
    foo_options = config.get_namespace('FOO_')
    assert 2 == len(foo_options)
    assert 'foo option 1' == foo_options['option_1']
    assert 'foo option 2' == foo_options['option_2']
    bar_options = config.get_namespace('BAR_', lowercase=False)
    assert 2 == len(bar_options)
    assert 'bar stuff 1' == bar_options['STUFF_1']
    assert 'bar stuff 2' == bar_options['STUFF_2']
    foo_options = config.get_namespace('FOO_', trim_namespace=False)
    assert 2 == len(foo_options)
    assert 'foo option 1' == foo_options['foo_option_1']
    assert 'foo option 2' == foo_options['foo_option_2']
    bar_options = config.get_namespace('BAR_', lowercase=False, trim_namespace=False)
    assert 2 == len(bar_options)
    assert 'bar stuff 1' == bar_options['BAR_STUFF_1']
    assert 'bar stuff 2' == bar_options['BAR_STUFF_2']
