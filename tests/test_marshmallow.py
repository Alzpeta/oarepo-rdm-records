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

from oarepo_rdm_records.marshmallow.dataset import DataSetMetadataSchemaV1


class MD(DataSetMetadataSchemaV1, marshmallow.Schema):
    pass


def test_marshmallow_app(app):
    "Test marshmallow with app"
    app.config.update(SUPPORTED_LANGUAGES=["cs", "en"])
    data = {"titles": {"cs": "jej"},
            "_created_by": 5,
            "publication_date": "2020-05-12",
            "creators": [{"given_name": "jmeno",
                          "family_name": "prijmeni",
                          "name": "prijmeni, jmeno",
                          "type": "personal"}],
            "_owners": [5],
            "resource_type": {"type": "schema"}}

    assert data == MD().load(data)

    data = {"titles": {"fr": "jej"},
            "_created_by": 5,
            "publication_date": "2020-05-12",
            "creators": [{'name': 'jmeno', "type": "personal"}],
            "_owners": [5],
            "resource_type": {"type": "schema"}}

    with pytest.raises(ValidationError):
        MD().load(data)


def test_marshmallow():
    """Test marshmallow."""


    data = {"titles":{"cs": "jej"},
            "_created_by": 5,
            "publication_date": "2020-05-12",
            "creators": [{"family_name": "prijmeno",
                          "given_name": "jmeno",
                          'name': 'prijmeno, jmeno',
                          "type": "personal"}],
            "_owners": [5],
            "resource_type": {"type": "schema"}}

    assert data == MD().load(data)

    data = {"titles": {"cs": "jej"},
            "abstract": {
                "description": {"cs": "jej"},
                "type": "abstract"
            },
            "rights": [{"rights": "free to play"}],
            "_created_by": 5,
            "publication_date": "2020-05-12",
            "creators": [{"given_name": "jmeno",
                          "family_name": "prijemno",
                          'name': 'prijemno, jmeno',
                          "type": "personal"}],
            "_owners": [5],
            "resource_type": {"type": "schema"}}

    assert data == MD().load(data)

    data = {"titles": {"css": "jej"},
            "_created_by": 5,
            "publication_date": "2020-05-12",
            "creators": [{'name': 'jmeno', "type": "Personal"}],
            "_owners": [5],
            "resource_type": {"type": "schema"}}

    with pytest.raises(ValidationError):
        MD().load(data)
