import json

import pytest
from jsonschema import ValidationError


# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# Invenio OpenID Connect is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
def get_schema():
    """This function loads the given schema available"""

    try:
        with open('../oarepo_rdm_records/jsonschemas/record-v1.0.0.json', 'r') as file:
            schema = json.load(file)
    except:
        with open('./oarepo_rdm_records/jsonschemas/record-v1.0.0.json', 'r') as file:
            schema = json.load(file)

    return schema

def test_json(app):
    """Test of json schema with app."""
    schema = app.extensions['invenio-records']

    data = json.loads('{"titles" : {"cs": "jej", "en": "yay"}, "descriptions":{"cs-cz": "jej"}}')
    schema.validate(data, get_schema())

    data = json.loads('{"subjects":[{"subject": {"cs":"neco", "en-us":"neco jinyho"}}]}')
    schema.validate(data, get_schema())

    data = json.loads('{"locations":[{"description": {"cs":"neco", "en-us":"neco jinyho"}, "place": "string"}]}')
    schema.validate(data, get_schema())

    data = json.loads('{"licenses":[{"license": {"cs":"neco", "en-us":"neco jinyho"}}]}')
    schema.validate(data, get_schema())

    data = json.loads('{"titles" : {"cs": "jej", "enn": "yay"}}')
    with pytest.raises(ValidationError):
        schema.validate(data, get_schema())

    data = json.loads('{"these": {"abstract" : {"css": "jej", "en": "yay"}}}')
    with pytest.raises(ValidationError):
        schema.validate(data, get_schema())

    data = json.loads('{"titles": "jej"}')
    with pytest.raises(ValidationError):
        schema.validate(data, get_schema())