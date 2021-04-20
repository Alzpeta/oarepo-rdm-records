# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""RDM record schemas."""
from marshmallow import Schema, fields
from marshmallow_utils.fields import SanitizedUnicode


class LanguageSchema(Schema):
    """Language schema."""

    id = SanitizedUnicode(required=True)
    title = fields.Raw(dump_only=True)
    description = fields.Raw(dump_only=True)
