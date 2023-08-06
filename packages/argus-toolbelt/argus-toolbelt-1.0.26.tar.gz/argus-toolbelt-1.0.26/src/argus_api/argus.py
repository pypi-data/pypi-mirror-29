"""Provides the wrapper class for Argus API"""
from os import mkdir
from os.path import dirname, join, sep, abspath, exists
from types import ModuleType
from time import time
from datetime import datetime

from argus_cli.settings import settings
from argus_api.helpers.log import log
from argus_api.helpers.module_loader import import_submodules
from argus_api.parsers import openapi2
from argus_api.helpers.generator import write_endpoints_to_disk

print(abspath(dirname(__file__)))
DEFAULT_API_DIRECTORY = join(abspath(dirname(__file__)), "api")
print(DEFAULT_API_DIRECTORY)


def load(swagger_files: list = settings["api"]["definitions"], parser: ModuleType = None, **kwargs) -> ModuleType:
    """Initializes the ArgusAPI, so that when called, the static API files will
    be generated to disk if they dont already exist, and the module then returned
    to the user. If the api module already exists, return the loaded module.

    :param base_url: Base URL to fetch the schema
    :param parser: Optional custom parser module for parsing the schema before writing to disk
    """

    # Attempt to load module api. This module doesn't exist by default,
    # and so on first run, this module will be generated
    parser = parser or openapi2
    
    try:
        import argus_api.api

        # If the time of generation is older than 2 days,
        # force regeneration
        time_ago = (datetime.now() - datetime.fromtimestamp(argus_api.api.__CREATED_AT__))
        if time_ago.days > 1:
            log.info("Argus API files are %d days old. Re-generating..." % time_ago.days)
            raise ModuleNotFoundError

    except ModuleNotFoundError:
        log.info("No static API files found")
        log.info("Generating swagger endpoints...")
        
        for schema in swagger_files:
            schema_location = "%s%s" % (settings["api"]["api_url"], schema)

            if not exists(DEFAULT_API_DIRECTORY):
                mkdir(DEFAULT_API_DIRECTORY)

            write_endpoints_to_disk(
                parser.load(schema_location),
                output=DEFAULT_API_DIRECTORY,
                with_plugin_decorators=True
            )
    finally:
        import argus_api.api
        import_submodules("argus_api.api", exclude_name="test_helpers")
        return argus_api.api
