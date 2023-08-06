#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ezedcfg` package."""

import pytest
from yaml.scanner import ScannerError
from yaml.constructor import ConstructorError
from ezedcfg import EZedCfg, UnrecognizedFormatError

# Before python 3.5 json.decoder raised an IOError rather than a JSONDecodeError
pre_35 = False
try:
    from json.decoder import JSONDecodeError
except ImportError:
    pre_35 = True

@pytest.fixture()
def setup_valid_yaml(tmpdir):
    """Returns a list containing three Vector instances"""
    test_config_data = """
    test: 1
    test2: 2
    """

    default_dict = {'test': 'testing', 'test2': 'still testing', 'test3': 123}

    test_cfg = tmpdir.mkdir("sub").join('test_config.yml')
    test_cfg.write(test_config_data)

    ez = EZedCfg(default_dict, str(test_cfg))

    return ez


@pytest.fixture()
def setup_valid_json(tmpdir):
    """Returns a list containing three Vector instances"""
    test_config_data = """
    {"test": 1, "test2": 2}
    """

    default_dict = {'test': 'testing', 'test2': 'still testing', 'test3': 123}

    test_cfg = tmpdir.mkdir("sub").join('test_config.yml')
    test_cfg.write(test_config_data)

    ez = EZedCfg(default_dict, str(test_cfg), file_format='json')

    return ez


@pytest.fixture()
def setup_invalid_yaml(tmpdir):
    """Returns a list containing three Vector instances"""
    test_config_data = """
    test: 1
    test2:
    1
    """

    default_dict = {'test': 'testing', 'test2': 'still testing'}

    test_cfg = tmpdir.mkdir("sub").join('test_config.yml')
    test_cfg.write(test_config_data)

    ez = EZedCfg(default_dict, str(test_cfg))

    return ez

@pytest.fixture()
def setup_dangerous_yaml(tmpdir):
    """Returns a list containing three Vector instances"""
    test_config_data = """
    test: 1
    test2: !!python/object/apply:subprocess.check_output ['ls']
    """

    default_dict = {'test': 'testing', 'test2': 'still testing', 'test3': 123}

    test_cfg = tmpdir.mkdir("sub").join('test_config.yml')
    test_cfg.write(test_config_data)

    ez = EZedCfg(default_dict, str(test_cfg))

    return ez

@pytest.fixture()
def setup_invalid_json(tmpdir):
    """Returns a list containing three Vector instances"""
    test_config_data = """
    {"test": 1, "test2": 2
    """

    default_dict = {'test': 'testing', 'test2': 'still testing', 'test3': 123}

    test_cfg = tmpdir.mkdir("sub").join('test_config.yml')
    test_cfg.write(test_config_data)

    ez = EZedCfg(default_dict, str(test_cfg), file_format='json')

    return ez


def test_initialise():
    ez = EZedCfg({'this-is-a-dict': 'yup'}, 'this/is/the/custom/config/path')
    assert ez.default_config == {
        'this-is-a-dict': 'yup'} and ez.config_path == 'this/is/the/custom/config/path'


def test_read(setup_valid_yaml):
    ez = setup_valid_yaml
    ez.read()
    assert ez.custom_config == {'test': 1, 'test2': 2}


def test_read_json(setup_valid_json):
    ez = setup_valid_json
    ez.read()
    assert ez.custom_config == {'test': 1, 'test2': 2}


def test_merge(setup_valid_yaml):
    ez = setup_valid_yaml
    ez.load()
    assert ez.merged_config == {'test': 1, 'test2': 2, "test3": 123}


def test_merge(setup_valid_json):
    ez = setup_valid_json
    ez.load()
    assert ez.merged_config == {'test': 1, 'test2': 2, "test3": 123}


def test_bad_format_param(setup_valid_yaml):
    with pytest.raises(UnrecognizedFormatError):
        ez = setup_valid_yaml
        ez.file_format = 'xml'
        ez.read()


def test_invalid_yaml(setup_invalid_yaml):
    with pytest.raises(ScannerError):
        ez = setup_invalid_yaml
        ez.load()

def test_dangerous_yaml(setup_dangerous_yaml):
    with pytest.raises(ConstructorError):
        ez = setup_dangerous_yaml
        ez.load()

def test_invalid_json(setup_invalid_json):
    if pre_35:
        with pytest.raises(ValueError):
            ez = setup_invalid_json
            ez.load()
    else:
        with pytest.raises(JSONDecodeError):
            ez = setup_invalid_json
            ez.load()

