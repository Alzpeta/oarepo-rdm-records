# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""RDM record schemas."""
from marshmallow import EXCLUDE, Schema, fields
from marshmallow_utils.schemas import IdentifierSchema as IS
from oarepo_taxonomies.marshmallow import TaxonomyField

from oarepo_rdm_records.marshmallow.mixins import TitledMixin
from oarepo_rdm_records.marshmallow.resource import ResourceType


class IdentifierSchema(Schema):
    """Identifier schema."""

    class Meta:
        """Meta attributes for the schema."""

        unknown = EXCLUDE

    material = fields.Str()
    scheme = fields.Str()
    value = fields.Str()
    status = fields.Str()


class RelatedIdentifierSchema(IS):
    """Related identifier schema."""

    SCHEMES = [
        "ark",
        # "arxiv",
        "bibcode",
        "doi",
        "ean13",
        "eissn",
        "handle",
        "igsn",
        "isbn",
        "issn",
        "istc",
        "lissn",
        "lsid",
        "pmid",
        "purl",
        "upc",
        "url",
        "urn",
        "w3id"
    ]

    def __init__(self, **kwargs):
        """Related identifier schema constructor."""
        super().__init__(allowed_schemes=self.SCHEMES, **kwargs)

    relation_type = TaxonomyField(mixins=[TitledMixin], required=True)
    resource_type = ResourceType()
