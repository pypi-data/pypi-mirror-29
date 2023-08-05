from os import mkdir
from os.path import join, exists, sep, abspath, dirname
from re import sub

from jinja2 import Environment, FileSystemLoader

JINJA_ENGINE = Environment(loader=FileSystemLoader(abspath(join(dirname(__file__), "..", "templates"))))

from argus_api.helpers.log import log

def write_endpoints_to_disk(endpoints, output, with_plugin_decorators=False) -> None:
    """Outputs the directory structure with all endpoints
    
    :param list endpoints: List of endpoints generated with build_endpoint_structure
    """
    EMPTY_INIT_FILE = ""

    log.info("Generating static API files to %s" % output)

    def find(key, dictionary):
        """Finds all occurances of a key in nested list
        """
        for k, v in dictionary.items():
            if k == key:
                yield v
            elif isinstance(v, dict):
                for result in find(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in find(key, d):
                        yield result
    
    endpoints = [endpoint for endpoint in find("__METADATA__", endpoints)]

    def create_python_module(path):
        if not exists(join(*path)):
            mkdir(join(*path))
        with open(join(*(path + ["__init__.py"])), "w") as init:
            init.write(
                JINJA_ENGINE.get_template("init.j2").render()
            )
    
    for endpoint in endpoints:
        path = [sep] + output.split(sep)

        # Create directory tree
        if not exists(join(*path)):
            mkdir(join(*path))
        with open(join(*(path + ["__init__.py"])), "w") as init:
            from time import time
            init.write(
                JINJA_ENGINE.get_template("init.j2").render() + 
                "\n__CREATED_AT__ = %f" % time()
            )
                

        for directory in endpoint["__PATH__"]:
            path.append(directory)
            
            # Write file
            if directory == endpoint["__PATH__"][-1]:
                log.info("Generating endpoint: %s" % "/".join(endpoint["__PATH__"][:-1]))
                with open(join(*(path[:-1] + ["%s.py" % endpoint["__MODULE_NAME__"]])), "w+") as endpoint_file:
                    method_names = []
                    endpoint_request_methods = []

                    # Never print the same method twice
                    for method in endpoint["__REQUEST_METHODS__"]:
                        if method.name not in method_names:
                            endpoint_request_methods.append(method)
                        method_names.append(method.name)

                    # Write endpoint templates to file, and decorate them
                    # with the plugin command registration decorator if with_plugin_decorators=True
                    endpoint_file.write(
                        JINJA_ENGINE.get_template("endpoint.j2").render(
                            endpoint=endpoint_request_methods,
                            path=endpoint["__PATH__"],
                            register_as_plugin=with_plugin_decorators
                        )
                    )
                log.info("Generating test helpers for endpoint: %s" % "/".join(endpoint["__PATH__"][:-1]))
                
                # Create a directory for test decorators
                create_python_module(path[:-1] + ["test_helpers"])
                create_python_module(path[:-1] + ["test_helpers", endpoint["__MODULE_NAME__"]])
                for request_method in endpoint["__REQUEST_METHODS__"]:
                    test_helper_path = path[:-1] + ["test_helpers", endpoint["__MODULE_NAME__"], "%s.py" % request_method.name]
                    # create_python_module(test_helper_path)
                    with open(join(*test_helper_path), "w") as test_helper:
                        test_helper.write(
                            JINJA_ENGINE.get_template("test_helpers/request.mock.j2").render(method=request_method)    
                        )

            else:
                # Create directory tree
                create_python_module(path)