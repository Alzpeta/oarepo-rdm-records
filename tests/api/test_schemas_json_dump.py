# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

from oarepo_rdm_records.marshmallow.dataset import DataSetMetadataSchemaV2
from oarepo_rdm_records.marshmallow.utils import dump_empty


def test_dumping_empty_record():
    empty_record = dump_empty(DataSetMetadataSchemaV2())

    assert empty_record == {
        '_access': {'access_condition': {'condition': None,
                                         'default_link_validity': None},
                    'access_right': None,
                    'embargo_date': None,
                    'files': None,
                    'metadata': None,
                    'owned_by': [None]},
        '_bucket': None,
        '_default_preview': None,
        '_created_by': None,
        '_schema': None,
        '_files': {},
        'keywords': [None],
        'language': {'code': None},
        '_owners': [None],
        'abstract': {'description': None, 'type': None},
        'additional_descriptions': [{'description': None, 'type': None}],
        'additional_titles': [None],
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
                'role': None,
                'type': None,
            }
        ],
        'dates': [
            {
                'type': None,
                'date': None,
                'description': None,
            }
        ],
        'id': None,
        'version': None,
        'publication_date': None,
        'references': [
            {
                'scheme': None,
                'reference': None,
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
        'rights': [{'identifier': None, 'rights': None, 'scheme': None, 'uri': None}],
        'titles': [None],
        # TODO: Investigate the impact of these 2 fields on
        #       frontend to backend to frontend flow
        'identifiers': [{'identifier': None, 'scheme': None}],
    }
