"""
GENERATOR PLUGIN
=====================

Generator is used to generate files based on templates — first and foremost, static API files. Generator creates the plugin hooks and redirects
to the appropriate generator methods, and can be run with:

argus-cli generate endpoint --name ENDPOINT_NAME -O api/folder/path
argus-cli generate endpoint --matching REGEX -O api/folder/path
argus-cli generate all

TODO: 
- Accept custom swagger.json URL
- Parse OAuth 3.0
- Resolve recursive references in JSONSchema
- Support different authentication modes from command line and generate authentication differently
- Templates for other languages
- Update API url from settings
"""
from os import mkdir, getcwd
from os.path import exists, join
from argus_api.helpers.generator import write_endpoints_to_disk
from argus_api.parsers.openapi2 import load
from argus_cli.settings import settings
from argus_cli.plugin import register_command


@register_command()
def all_endpoints(directory: str) -> list:
    """Generates all endpoints to a given directory
    
    :param directory: Output directory
    """
    path = join(getcwd(), directory)
    for schema in settings["api"]["definitions"]:
        schema_location = "%s%s" % (settings["api"]["api_url"], schema)

        if not exists(path):
            mkdir(path)

        write_endpoints_to_disk(
            load(schema_location),
            output=path
        )
