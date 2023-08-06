# -*- coding: utf-8 -*-

"""Main module."""
import logging
import json
import yaml


class EZedCfg:
    def __init__(self, default_config, config_path, file_format='yaml'):
        """

        Args:
            default_config: (dict) A dictionary containing the default
                configuration values.
            config_path: (string) A string containing the path (abs or relative)
                to the desired custom config file.
            file_format: (string) String indicating whether a file is JSON
                (json) or YAML (yaml) formatted
        """
        self.default_config = default_config
        self.config_path = config_path
        self.file_format = file_format.lower().strip()
        self.merged_config = False
        self.custom_config = False

    def read(self):
        """This method attempts to load the file supplied in the config_path parameter.

        Raises:
            UnrecognizedFormatError: If an unknown file format is specified in
            the file_format parameter

        Returns:
            dict: A dict containing the data in the supplied configuration file.

        """

        with open(self.config_path, 'r') as config_file:
            config_string = config_file.read()

        if self.file_format == 'json':
            self.custom_config = json.loads(config_string)
        elif self.file_format == 'yaml':
            self.custom_config = yaml.safe_load(config_string)
        else:
            raise UnrecognizedFormatError(
                'File format ({}) not recognised'.format(str(self.file_format)))

        return self.custom_config

    def merge(self):
        """This method merges the default configuration and the supplied configuration

        Returns:
            dict:  A dict containing the updated configuration.

        """
        if self.custom_config is not False:
            # Retain the unchanged default config.
            self.merged_config = self.default_config
            return self.merged_config.update(self.custom_config)

    def load(self):
        """This method runs the entire file reading and dictionary merging process

        This is the primary entry point for this module as it returns the merged
        configuration.

        Returns:
            dict: A dictionary containing the merged configuration data.

        """

        self.read()
        self.merge()
        return self.merged_config


class UnrecognizedFormatError(Exception):
    """A simple exception raised when an unrecognized encoding
    format is supplied.
    """
    def __init__(self, msg=None):
        if msg is None:
            msg = "Unknown file formatting."
