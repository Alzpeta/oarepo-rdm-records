# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""RDM record schemas."""

from flask_babelex import lazy_gettext as _
from marshmallow import validate
from marshmallow_utils.fields import SanitizedUnicode
from marshmallow_utils.schemas import IdentifierSchema


class RightsSchema(IdentifierSchema):
    """License rights schema."""

    def __init__(self, **kwargs):
        """Rights schema constructor."""
        super().__init__(
            fail_on_unknown=False, identifier_required=False, **kwargs)

    id = SanitizedUnicode()
    title = SanitizedUnicode()
    description = SanitizedUnicode()
    link = SanitizedUnicode(
        validate=validate.URL(error=_('Not a valid URL.'))
    )
