# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""RDM record schemas."""

from marshmallow_utils.fields import SanitizedUnicode
from marshmallow_utils.schemas import IdentifierSchema

from oarepo_rdm_records.config import RDM_RECORDS_IDENTIFIERS_SCHEMES


class SubjectSchema(IdentifierSchema):
    """Subject schema."""

    def __init__(self, **kwargs):
        """SubjectSchema."""
        super().__init__(
             identifier_required=False, allowed_schemes=RDM_RECORDS_IDENTIFIERS_SCHEMES, **kwargs)

    subject = SanitizedUnicode(required=True)
