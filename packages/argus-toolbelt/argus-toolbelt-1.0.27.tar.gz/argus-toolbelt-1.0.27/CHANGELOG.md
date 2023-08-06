CHANGELOG
-----------------------------------------------

### 0.9.2

#### Features
- `setup.py` has been updated to allow installing all packages
- Sphinx documentation has been added
- Script for converting markdown files to rST and include them in Sphinx
- `src/plugins` is now its own package, called `argus_plugins`

### 0.9.1

#### Bugs
- [argus_api] Fixed bug where responses would not be correctly printed in generated function docstrings
- [argus_cli] Fixed bug where help text would crash if it containes %, \{ or \} characters due to argparse considering them formatting characters

#### Features
- [argus_api] New decorators: `@authentication.with_credentials()`, `@authentication.with_api_key()`
- [argus_api] New helpers `helpers/tests` provides decorator factory for mocking HTTP requests, and generating fake responses
- [argus_api] Support for extending API definition parsing
- [argus_api] `parsers` directory holds different API definition parsers (currently only `openapi2` (swagger))
- [argus_api] `RequestMethod` ABC for creating functions (as template strings or callables) from method definitions
- [plugins] `generator` is now a core functionality of `argus_api`

#### Improvements
- [argus_api] Split up monolith `swagger.py` into multiple files
- [argus_api] Function annotations and docstrings have been added where these were previously missing
- [argus_api] Supports different kinds of parsers, allowing extensions for RABL, OpenAPI 3.0, and other formats
- [argus_api] Removed references to "Swagger" to avoid 'locking' us to swagger
- [argus_api] `api.py` -> `argus.py`: Wrapper for loading previously generated API files, or generate new API files
- [argus_api] Helpers have been split up:
  -  `helpers/http_helpers` -> `helpers/urls` for URL parsing, and `helpers/http` for requests
