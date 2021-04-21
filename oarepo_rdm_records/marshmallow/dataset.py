# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""RDM record schemas."""
from datetime import timezone
from functools import partial

from flask_babelex import lazy_gettext as _
from invenio_records_rest.schemas import StrictKeysMixin
from marshmallow import fields, pre_load, validate, validates, post_dump, Schema
from marshmallow.schema import BaseSchema
from marshmallow_utils.fields import (
    EDTFDateString,
    IdentifierSet,
    SanitizedHTML,
    SanitizedUnicode, NestedAttribute,
)
from marshmallow_utils.fields import TZDateTime, Links
from marshmallow_utils.permissions import FieldPermissionsMixin
from oarepo_invenio_model.marshmallow import (
    InvenioRecordMetadataFilesMixin,
    InvenioRecordMetadataSchemaV1Mixin,
)
from oarepo_multilingual.marshmallow import MultilingualStringV2
from oarepo_rdm_records.marshmallow.access import AccessSchema
from oarepo_rdm_records.marshmallow.dates import DateSchema
from oarepo_rdm_records.marshmallow.identifier import (
    IdentifierSchema,
    RelatedIdentifierSchema,
)
from oarepo_rdm_records.marshmallow.language import LanguageSchema
from oarepo_rdm_records.marshmallow.person import ContributorSchema, CreatorSchema
from oarepo_rdm_records.marshmallow.pids import PIDSchema
from oarepo_rdm_records.marshmallow.reference import ReferenceSchema
from oarepo_rdm_records.marshmallow.resource import ResourceType
from oarepo_rdm_records.marshmallow.rights import RightsSchema
from oarepo_rdm_records.marshmallow.subject import SubjectSchema


class DataSetMetadataSchemaV2(InvenioRecordMetadataFilesMixin,
                              InvenioRecordMetadataSchemaV1Mixin,
                              StrictKeysMixin):
    """DataSet metaddata schema."""

    resource_type = ResourceType(required=True)
    creators = fields.List(
        fields.Nested(CreatorSchema),
        required=True,
        validate=validate.Length(
            min=1, error=_("Missing data for required field.")
        )
    )
    title = MultilingualStringV2(required=True)
    additional_titles = fields.List(MultilingualStringV2())
    publisher = SanitizedUnicode()
    publication_date = EDTFDateString(required=True)
    subjects = fields.List(fields.Nested(SubjectSchema))
    contributors = fields.List(fields.Nested(ContributorSchema))
    dates = fields.List(fields.Nested(DateSchema))
    languages = fields.List(fields.Nested(LanguageSchema))
    # alternate identifiers
    identifiers = IdentifierSet(
        fields.Nested(partial(IdentifierSchema, fail_on_unknown=False))
    )
    related_identifiers = fields.List(fields.Nested(RelatedIdentifierSchema))
    version = SanitizedUnicode()
    rights = fields.List(fields.Nested(RightsSchema))
    abstract = MultilingualStringV2(required=True)  # WARNING: May contain user-input HTML
    additional_descriptions = fields.List(MultilingualStringV2())
    references = fields.List(fields.Nested(ReferenceSchema))
    pids = fields.Dict(keys=fields.String(), values=fields.Nested(PIDSchema))
    access = NestedAttribute(AccessSchema)

    @pre_load
    def sanitize_html_fields(self, data, **kwargs):
        """Sanitize fields that may contain user-input HTML strings."""
        if 'abstract' in data:
            for lang, val in data.get('abstract').items():
                raw = data['abstract'][lang]
                data['abstract'][lang] = SanitizedHTML()._deserialize(raw, 'abstract', data)

        return data

    @validates("pids")
    def validate_pids(self, value):
        """Validates the keys of the pids are supported providers."""
        for scheme, pid_attrs in value.items():
            # The required flag applies to the identifier value
            # It won't fail for empty allowing the components to reserve one
            id_schema = IdentifierSchema(
                fail_on_unknown=False, identifier_required=True)
            id_schema.load({
                "scheme": scheme,
                "identifier": pid_attrs.get("identifier")
            })
