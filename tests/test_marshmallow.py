# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# Invenio OpenID Connect is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
from __future__ import absolute_import, print_function

import marshmallow
import pytest
from marshmallow import ValidationError

from oarepo_rdm_records.marshmallow.dataset import DataSetMetadataSchemaV2


class MD(DataSetMetadataSchemaV2, marshmallow.Schema):
    pass


def test_marshmallow_app(app, db):
    """Test marshmallow with app."""
    app.config.update(SUPPORTED_LANGUAGES=["cs", "en"])
    data = {"title": {"cs": "jej"},
            "abstract": {"cs": "joj"},
            "languages": [{"links": {"self": "http://localhost/2.0/taxonomies/languages/cze"}}],
            "publication_date": "2020-05-12",
            "creators": [{'person_or_org': {"given_name": "jmeno",
                                            "family_name": "prijmeni",
                                            "name": "prijmeni, jmeno",
                                            "type": "personal"}}],
            "resource_type": {"type": {"links": {"self": "http://localhost/2.0/taxonomies/resourceType/datasets"}}}}

    resolved = MD().load(data)
    data.pop('resource_type')
    data.pop('languages')
    resolved.pop('resource_type')
    resolved.pop('languages')
    assert data == resolved

    data = {"title": {"fr": "jej"},
            "_created_by": 5,
            "publication_date": "2020-05-12",
            "creators": [{'name': 'jmeno', "type": "personal"}],
            "resource_type": {"type": {"links": {"self": "http://localhost/2.0/taxonomies/resourceType/datasets"}}}}

    with pytest.raises(ValidationError):
        MD().load(data)


def test_marshmallow():
    """Test marshmallow."""

    data = {"title": {"cs": "jej"},
            "abstract": {"cs": "jjo"},
            "publication_date": "2020-05-12",
            "creators": [{'person_or_org': {"family_name": "prijmeno",
                                            "given_name": "jmeno",
                                            'name': 'prijmeno, jmeno',
                                            "type": "personal"}}],
            "resource_type": {"type": {"links": {"self": "http://localhost/2.0/taxonomies/resourceType/datasets"}}}}

    resolved = MD().load(data)
    data.pop('resource_type')
    resolved.pop('resource_type')
    assert data == resolved

    data = {"title": {"cs": "jej"},
            "abstract": {"cs": "jej"},
            "rights": [{'links': {'self': 'http://localhost/2.0/taxonomies/licenses/copyright'}}],
            "publication_date": "2020-05-12",
            "creators": [{'person_or_org': {"given_name": "jmeno",
                                            "family_name": "prijemno",
                                            'name': 'prijemno, jmeno',
                                            "type": "personal"}}],
            "resource_type": {"type": {"links": {"self": "http://localhost/2.0/taxonomies/resourceType/datasets"}}}}
    resolved = MD().load(data)
    data.pop('rights')
    data.pop('resource_type')
    resolved.pop('rights')
    resolved.pop('resource_type')
    assert data == resolved

    data = {"title": {"css": "jej"},
            "publication_date": "2020-05-12",
            "creators": [{'person_or_org': {'name': 'jmeno', "type": "Personal"}}],
            "resource_type": {"type": {"links": {"self": "http://localhost/2.0/taxonomies/resourceType/datasets"}}}}

    with pytest.raises(ValidationError):
        MD().load(data)
