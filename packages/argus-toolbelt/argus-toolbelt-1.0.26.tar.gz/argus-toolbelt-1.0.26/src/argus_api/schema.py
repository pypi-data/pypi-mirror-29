import time, re, json, requests
from os.path import join, abspath, exists, dirname, basename
from collections import OrderedDict

from requests.exceptions import HTTPError
from jsonschema import RefResolver

from argus_api.helpers.log import log

DEFAULT_API_DEFINITION_LOCATION = join(abspath(dirname(__file__)), "..", "argus_cli", "resources")


def write_schema_to_disk(schema: dict, name: str = "api-definition.json") -> None:
    """Saves swagger data to the local filesystem with current timestamp.
    It currently saves it to %cwd%/DEFAULT_API_DEFINITION_LOCATION

    :param dict schema: JSON data
    """
    schema["timestamp"] = int(time.time())

    log.info("Saving swagger file back to filesystem...")
    with open(join(DEFAULT_API_DEFINITION_LOCATION, name), 'w') as f:
        json.dump(schema, f)


def find_schema(location: str, name: str = None) -> dict:
    """Loads JSON schema from a file or URL

    :param location: Location of the swagger file
    :param name: Optional name of schema
    :returns: Swagger JSON in a dict
    """
    schema = {"timestamp": None}

    
    # Check if it is a file on the local filesystem
    if exists(location):
        schema = json.load(open(location), object_pairs_hook=OrderedDict)

    # If the given location is a URL, create a name for the schema,
    # then check if this schema is already fetched, and if the timestamp
    # is more recent than a day. If it is, just return the schema, otherwise
    # fetch the schema again and store it with a new timestamp.
    elif re.match(r"^https?:\/\/", location):
        # Name the schema from the URI, e.g https://api.mnemonic.no/customers/swagger.json -> customers-swagger.json
        schema_name = "-".join([
            word
            for word in re.split(r"[/\/]", re.match("https?:\/\/(?:.+?)(\/.*)", location).groups()[0])
            if word
        ])

        if exists(join(DEFAULT_API_DEFINITION_LOCATION, schema_name)):
            schema = json.load(
                open(join(DEFAULT_API_DEFINITION_LOCATION, schema_name)),
                object_pairs_hook=OrderedDict
            )
        if "timestamp" not in schema or not schema["timestamp"] or (int(time.time()) - schema["timestamp"]) > 86400:
            response = requests.get(location)
            schema = response.json(object_pairs_hook=OrderedDict)
            if not response.ok:
                raise HTTPError(
                    "Error while retrieving swagger json from %s. (Status: %s)"
                    % (location, response.status_code)
                )
            write_schema_to_disk(schema, name=schema_name)

    elif location[0:7] != "http://" and location[0:8] != "https://":
        raise ValueError("The API schema location is not a valid address or path on the filesystem: %s" % location)

    return schema

