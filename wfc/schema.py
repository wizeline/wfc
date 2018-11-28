import json

import jsonschema
from jsonschema.exceptions import ValidationError

from wfc.commons import asset_path
from wfc.errors import SchemaViolationError
from wfc.types import OutputVersion


class SchemaValidator:
    def __init__(self):
        self._schemas = {}

    def _load_output_schema(self, version):
        if version not in self._schemas:
            if version == OutputVersion.V21:
                schema_file = 'schema21.json'
            elif version == OutputVersion.V20:
                schema_file = 'schema.json'
            else:
                raise ValueError('Invalid version', version)

            with open(asset_path(schema_file)) as schema:
                self._schemas[version] = json.load(schema)

        return self._schemas[version]

    def _has_valid_version(self, script):
        return 'version' in script and OutputVersion.is_valid(
            script['version']
        )

    def execute(self, script):
        is_valid = False

        if not isinstance(script, dict):
            raise TypeError('script has to be a dict')

        if self._has_valid_version(script):
            version = OutputVersion(script['version'])
            schema = self._load_output_schema(version)
            try:
                jsonschema.validate(script, schema)
            except ValidationError as error:
                raise SchemaViolationError(error, script, version)

            is_valid = True

        return is_valid
