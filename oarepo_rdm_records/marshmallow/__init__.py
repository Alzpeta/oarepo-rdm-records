# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CESNET Prague.
#
# CIS theses repository is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Schemas for marshmallow."""

from .access import AccessSchema
from .dates import DateSchema
from .identifier import RelatedIdentifierSchema
from .language import LanguageSchema
from .person import (
    ContributorSchema,
)
from .pids import PIDSchema
from .reference import ReferenceSchema
from .rights import RightsSchema

__all__ = ('AccessSchema',
           'DateSchema',
           'RelatedIdentifierSchema', 'LanguageSchema',
           'ContributorSchema',
           'PIDSchema', 'ReferenceSchema', 'RightsSchema')
