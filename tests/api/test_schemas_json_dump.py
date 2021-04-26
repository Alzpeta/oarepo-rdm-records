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
        '_bucket': None,
        '_files': {},
        'access': {'embargo': {'active': None, 'reason': None, 'until': None},
                   'files': None,
                   'owned_by': [{'user': None}],
                   'record': None},
        '_schema': None,
        'abstract': None,
        'additional_descriptions': [None],
        'additional_titles': [None],
        'contributors': [{'affiliations': [{'identifiers': [{'identifier': None,
                                                             'scheme': None}],
                                            'name': None}],
                          'person_or_org': {'family_name': None,
                                            'given_name': None,
                                            'identifiers': [None],
                                            'name': None,
                                            'type': None},
                          'role': None}],
        'creators': [{'affiliations': [{'identifiers': [{'identifier': None,
                                                         'scheme': None}],
                                        'name': None}],
                      'person_or_org': {'family_name': None,
                                        'given_name': None,
                                        'identifiers': [None],
                                        'name': None,
                                        'type': None},
                      'role': None}],
        'dates': [{'date': None, 'description': None, 'type': None}],
        'id': None,
        'identifiers': [None],
        'keywords': [None],
        'languages': None,
        'pids': None,
        'publication_date': None,
        'publisher': None,
        'references': [{'identifier': None, 'reference': None, 'scheme': None}],
        'related_identifiers': [{'identifier': None,
                                 'relation_type': None,
                                 'resource_type': None,
                                 'scheme': None}],
        'resource_type': None,
        'rights': None,
        'subjects': [{'identifier': None, 'scheme': None, 'subject': None}],
        'title': None,
        'version': None
    }
