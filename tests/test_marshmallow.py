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

from oarepo_rdm_records.marshmallow.json import MetadataSchemaV1


class MD(MetadataSchemaV1, marshmallow.Schema):
    pass

def test_marshmallow_app(app):
    "Test marshmallow with app"
    app.config.update(SUPPORTED_LANGUAGES=["cs", "en"])
    data = {"titles": {"cs": "jej"},
            "_created_by": 5,
            "_access": {"files_restricted": False, "metadata_restricted": False},
            "publication_date": "2020-05-12",
            '_publication_date_search': '2020-05-12',
            "creators": [{'name': 'jmeno', "type": "Personal"}],
            "_owners": [5],
            "access_right": "cosi",
            "resource_type": {"type": "schema"}}

    assert data == MD().load(data)

    data = {"titles": {"fr": "jej"},
            "_created_by": 5,
            "_access": {"files_restricted": False, "metadata_restricted": False},
            "publication_date": "2020-05-12",
            '_publication_date_search': '2020-05-12',
            "creators": [{'name': 'jmeno', "type": "Personal"}],
            "_owners": [5],
            "access_right": "cosi",
            "resource_type": {"type": "schema"}}

    with pytest.raises(ValidationError):
        MD().load(data)


def test_marshmallow():
    """Test marshmallow."""


    data = {"titles":{"cs": "jej"},
            "_created_by": 5,
            "_access": {"files_restricted": False, "metadata_restricted": False},
            "publication_date": "2020-05-12",
            '_publication_date_search': '2020-05-12',
            "creators": [{'name': 'jmeno', "type": "Personal"}],
            "_owners": [5],
            "access_right": "cosi",
            "resource_type": {"type": "schema"}}

    assert data == MD().load(data)

    data = {"titles": {"cs": "jej"},
            "descriptions": {"cs": "jej"},
            "subjects": [{"subject": {"cf-cz": "jej", "en": "yaay"}}],
            "licenses": [{"license": {"cs-cz": "jej", "en": "yaay"}}],
            "locations": [{"description":{"cs-cz": "jej", "en": "yaay"}, "place": "cosi"}],
            "_created_by": 5,
            "_access": {"files_restricted": False, "metadata_restricted": False},
            "publication_date": "2020-05-12",
            '_publication_date_search': '2020-05-12',
            "creators": [{'name': 'jmeno', "type": "Personal"}],
            "_owners": [5],
            "access_right": "cosi",
            "resource_type": {"type": "schema"}}

    assert data == MD().load(data)

    data = {"titles": {"css": "jej"},
            "_created_by": 5,
            "_access": {"files_restricted": False, "metadata_restricted": False},
            "publication_date": "2020-05-12",
            '_publication_date_search': '2020-05-12',
            "creators": [{'name': 'jmeno', "type": "Personal"}],
            "_owners": [5],
            "access_right": "cosi",
            "resource_type": {"type": "schema"}}

    with pytest.raises(ValidationError):
        MD().load(data)
