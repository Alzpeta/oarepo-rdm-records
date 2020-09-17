# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

import os

from flask_babelex import lazy_gettext as _

from oarepo_rdm_records.marshmallow.json import MetadataSchemaV1, dump_empty

#from oarepo_rdm_records.vocabularies import Vocabularies


def test_dumping_empty_record():
    empty_record = dump_empty(MetadataSchemaV1())

    assert empty_record == {
        '_access': {'files_restricted': None, 'metadata_restricted': None},
        '_default_preview': None,
        '_communities': None,
        '_contact': None,
        '_created_by': None,
        '_embargo_date': None,
        '_files': [
            {
                'bucket': None,
                'checksum': None,
                'key': None,
                'links': None,
                'size': None,
                'type': None
            }
        ],
        '_internal_notes': [
            {
                'user': None,
                'timestamp': None,
                'note': None
            }
        ],
        '_owners': [None],
        'access_right': None,
        'contributors': [
            {
                'affiliations': [
                    {
                        'name': None,
                        'identifiers': None,
                    }
                ],
                'family_name': None,
                'given_name': None,
                'identifiers': None,
                'name': None,
                'role': None,
                'type': None,
            }
        ],
        'creators': [
            {
                'affiliations': [
                    {
                        'name': None,
                        'identifiers': None,
                    }
                ],
                'family_name': None,
                'given_name': None,
                'identifiers': None,
                'name': None,
                'type': None,
            }
        ],
        'dates': [
            {
                'type': None,
                'end': None,
                'description': None,
                'start': None
            }
        ],
        'extensions': None,
        'descriptions': None,
        'language': None,
        'locations': [
            {
                'description': None,
                'point': {
                    'lon': None,
                    'lat': None
                },
                'place': None
            }
        ],
        'licenses': [
            {
                'identifier': None,
                'scheme': None,
                'uri': None,
                'license': None
            }
        ],
        'version': None,
        'publication_date': None,
        'references': [
            {
                'scheme': None,
                'reference_string': None,
                'identifier': None
            }
        ],
        'related_identifiers': [
            {
                'resource_type': {
                    'subtype': None,
                    'type': None
                },
                'scheme': None,
                'relation_type': None,
                'identifier': None
            }
        ],
        'resource_type': {
            'subtype': None,
            'type': None
        },
        'subjects': [{'subject': None, 'identifier': None, 'scheme': None}],
        'titles': None,
        # TODO: Investigate the impact of these 2 fields on
        #       frontend to backend to frontend flow
        'identifiers': None,
        'recid': None
    }

