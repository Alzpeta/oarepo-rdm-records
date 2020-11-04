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
        with open('test_module/jsonschemas/test/test-v1.0.0.json', 'r') as file:
            schema = json.load(file)
    except:
        with open('./tests/test_module/jsonschemas/test/test-v1.0.0.json', 'r') as file:
            schema = json.load(file)

    return schema

def test_json(app):
    """Test of json schema with app."""
    schema = app.extensions['invenio-records']

    data = json.loads('{"these": {"titles" : {"cs": "jej", "en": "yay"}}}')
    schema.validate(data, get_schema())

    # data = json.loads('{"these": {"abstract" : {"cs": "jej", "en": "yay"}, "contributor" : "Alzbeta Pokorna", "modified":"2012-04-23T18:25:43.511Z"}}')
    # schema.validate(data, get_schema())
    #
    # data = json.loads('{"these": {"abstract" : 1}}')
    # with pytest.raises(ValidationError):
    #     schema.validate(data, get_schema())
    #
    # data = json.loads('{"these": {"abstract" : {"css": "jej", "en": "yay"}}}')
    # with pytest.raises(ValidationError):
    #     schema.validate(data, get_schema())