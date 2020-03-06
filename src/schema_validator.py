import os
import json

from jsonschema import validate

TEMPLATES_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "schemas")
)


def validate_request(json_input, schema):
    validate(json_input, json.load(open(os.path.join(TEMPLATES_PATH, "%s.schema" % schema))))
