# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2020 CERN.
# Copyright (C) 2019-2020 Northwestern University.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Tests for Invenio RDM Records JSON Schemas."""
import os

import pytest
from invenio_records_rest.schemas.fields import DateString, SanitizedUnicode
from marshmallow import ValidationError
from marshmallow.fields import Bool, Integer, List

from oarepo_rdm_records.marshmallow.json import (
    AffiliationSchemaV1,
    ContributorSchemaV1,
    CreatorSchemaV1,
    DateSchemaV1,
    DescriptionSchemaV1,
    InternalNoteSchemaV1,
    LicenseSchemaV1,
    LocationSchemaV1,
    MetadataSchemaV1,
    PointSchemaV1,
    ReferenceSchemaV1,
    RelatedIdentifierSchemaV1,
    ResourceTypeSchemaV1,
    SubjectSchemaV1,
    TitleSchemaV1,
)
from oarepo_rdm_records.metadata_extensions import MetadataExtensions


def test_affiliations():
    """Test affiliations schema."""
    valid_full = {
        "name": "Entity One",
        "identifiers": {
            "ror": "03yrm5c26"
        }
    }
    data = AffiliationSchemaV1().load(valid_full)
    assert data == valid_full

    invalid_no_name = {
        "identifiers": {
            "ror": "03yrm5c26"
        }
    }
    with pytest.raises(ValidationError):
        data = AffiliationSchemaV1().load(invalid_no_name)

    invalid_identifier = {
        "name": "Entity One",
        "identifiers": {
            "ror": ""
        }
    }
    with pytest.raises(ValidationError):
        data = AffiliationSchemaV1().load(invalid_identifier)

    invalid_scheme = {
        "name": "Entity One",
        "identifiers": {
            "": "03yrm5c26"
        }
    }
    with pytest.raises(ValidationError):
        data = AffiliationSchemaV1().load(invalid_scheme)


def test_creator():
    """Test creator schema."""
    # If present, bare minimum
    valid_minimal = {
        "name": "Julio Cesar",
        "type": "Personal"
    }
    data = CreatorSchemaV1().load(valid_minimal)
    assert data == valid_minimal

    # Full person
    valid_full_person = {
        "name": "Julio Cesar",
        "type": "Personal",
        "given_name": "Julio",
        "family_name": "Cesar",
        "identifiers": {
            "Orcid": '0000-0002-1825-0097',
        },
        "affiliations": [{
            "name": "Entity One",
            "identifiers": {
                "ror": "03yrm5c26"
            }
        }]
    }
    data = CreatorSchemaV1().load(valid_full_person)
    assert data == valid_full_person

    # Full organization
    valid_full_org = {
        "name": "California Digital Library",
        "type": "Organizational",
        "identifiers": {
            "ror": "03yrm5c26",
        },
        # "given_name", "family_name" and "affiliations" are ignored if passed
        "family_name": "I am ignored!"
    }
    data = CreatorSchemaV1().load(valid_full_org)
    assert data == valid_full_org

    invalid_no_name = {
        "type": "Personal",
        "given_name": "Julio",
        "family_name": "Cesar",
        "identifiers": {
            "Orcid": "0000-0002-1825-0097",
        },
        "affiliations": [{
            "name": "Entity One",
            "identifiers": {
                "ror": "03yrm5c26"
            }
        }]
    }
    with pytest.raises(ValidationError):
        data = CreatorSchemaV1().load(invalid_no_name)

    invalid_no_type = {
        "name": "Julio Cesar",
    }
    with pytest.raises(ValidationError):
        data = CreatorSchemaV1().load(invalid_no_type)

    invalid_type = {
        "name": "Julio Cesar",
        "type": "Invalid",
    }
    with pytest.raises(ValidationError):
        data = CreatorSchemaV1().load(invalid_type)

    invalid_scheme = {
        "name": "Julio Cesar",
        "type": "Personal",
        "identifiers": {
            "unapproved scheme": "0000-0002-1825-0097",
        }
    }
    with pytest.raises(ValidationError):
        data = CreatorSchemaV1().load(invalid_type)

    invalid_orcid_identifier = {
        "name": "Julio Cesar",
        "type": "Personal",
        "identifiers": {
            # NOTE: This *is* an invalid ORCiD
            "Orcid": "9999-9999-9999-9999",
        }
    }
    with pytest.raises(ValidationError):
        data = CreatorSchemaV1().load(invalid_orcid_identifier)

    invalid_ror_identifier = {
        "name": "Julio Cesar Empire",
        "type": "Organizational",
        "identifiers": {
            "ror": "9999-9999-9999-9999",
        }
    }
    with pytest.raises(ValidationError):
        data = CreatorSchemaV1().load(invalid_ror_identifier)

    invalid_identifier_for_person = {
        "name": "Julio Cesar",
        "type": "Personal",
        "identifiers": {
            "ror": "03yrm5c26"
        }
    }
    with pytest.raises(ValidationError):
        data = CreatorSchemaV1().load(invalid_identifier_for_person)

    invalid_identifier_for_org = {
        "name": "Julio Cesar Empire",
        "type": "Organizational",
        "identifiers": {
            "Orcid": "0000-0002-1825-0097",
        }
    }
    with pytest.raises(ValidationError):
        data = CreatorSchemaV1().load(invalid_identifier_for_org)


def test_contributor():
    """Test contributor schema."""
    valid_full = {
        "name": "Julio Cesar",
        "type": "Personal",
        "given_name": "Julio",
        "family_name": "Cesar",
        "identifiers": {
            "Orcid": "0000-0002-1825-0097",
        },
        "affiliations": [{
            "name": "Entity One",
            "identifiers": {
                "ror": "03yrm5c26"
            }
        }],
        "role": "RightsHolder"
    }

    data = ContributorSchemaV1().load(valid_full)
    assert data == valid_full

    valid_minimal = {
        "name": "Julio Cesar",
        "type": "Personal",
        "role": "RightsHolder"
    }

    data = ContributorSchemaV1().load(valid_minimal)
    assert data == valid_minimal

    invalid_no_name = {
        "type": "Personal",
        "given_name": "Julio",
        "family_name": "Cesar",
        "identifiers": {
            "Orcid": "0000-0002-1825-0097",
        },
        "role": "RightsHolder"
    }
    with pytest.raises(ValidationError):
        data = ContributorSchemaV1().load(invalid_no_name)

    invalid_no_name_type = {
        "name": "Julio Cesar",
        "given_name": "Julio",
        "family_name": "Cesar",
        "identifiers": {
            "Orcid": "0000-0002-1825-0097",
        },
        "role": "RightsHolder"
    }
    with pytest.raises(ValidationError):
        data = ContributorSchemaV1().load(invalid_no_name_type)

    invalid_name_type = {
        "name": "Julio Cesar",
        "type": "Invalid",
        "given_name": "Julio",
        "family_name": "Cesar",
        "identifiers": {
            "Orcid": "0000-0002-1825-0097",
        },
        "role": "RightsHolder"
    }
    with pytest.raises(ValidationError):
        data = ContributorSchemaV1().load(invalid_name_type)

    invalid_no_role = {
        "name": "Julio Cesar",
        "type": "Personal",
        "given_name": "Julio",
        "family_name": "Cesar",
        "identifiers": {
            "Orcid": "0000-0002-1825-0097",
        },
    }
    with pytest.raises(ValidationError):
        data = ContributorSchemaV1().load(invalid_no_role)

def test_internal_note():
    """Test internal note schema."""
    valid_full = {
        "user": "inveniouser",
        "note": "RDM record",
        "timestamp": "2020-02-01"
    }
    data = InternalNoteSchemaV1().load(valid_full)
    assert data == valid_full

    invalid_no_user = {
        "note": "RDM record",
        "timestamp": "2020-02-01"
    }
    with pytest.raises(ValidationError):
        data = InternalNoteSchemaV1().load(invalid_no_user)

    invalid_no_note = {
        "user": "inveniouser",
        "timestamp": "2020-02-01"
    }
    with pytest.raises(ValidationError):
        data = InternalNoteSchemaV1().load(invalid_no_note)

    invalid_no_timestamp = {
        "user": "inveniouser",
        "note": "RDM record"
    }
    with pytest.raises(ValidationError):
        data = InternalNoteSchemaV1().load(invalid_no_timestamp)

    invalid_timestamp = {
        "user": "inveniouser",
        "note": "RDM record",
        "timestamp": "01/02/2020"
    }
    with pytest.raises(ValidationError):
        data = InternalNoteSchemaV1().load(invalid_timestamp)


def test_license():
    """Test license scehma."""
    valid_full = {
        "license": {"en":"Copyright Maximo Decimo Meridio 2020. Long statement"},
        "uri": "https://opensource.org/licenses/BSD-3-Clause",
        "identifier": "BSD-3",
        "scheme": "BSD-3"
    }

    data = LicenseSchemaV1().load(valid_full)
    assert data == valid_full

    valid_minimal = {
        "license": {"en":"Copyright Maximo Decimo Meridio 2020. Long statement"}
    }

    data = LicenseSchemaV1().load(valid_minimal)
    assert data == valid_minimal

    invalid_no_license = {
        "uri": "https://opensource.org/licenses/BSD-3-Clause",
        "identifier": "BSD-3",
        "scheme": "BSD-3"
    }
    with pytest.raises(ValidationError):
        data = LicenseSchemaV1().load(invalid_no_license)


def test_subject():
    """Test subject schema."""
    valid_full = {
        "subject": {"cs":"Romans"},
        "identifier": "subj-1",
        "scheme": "no-scheme"
    }

    data = SubjectSchemaV1().load(valid_full)
    assert data == valid_full

    valid_minimal = {
        "subject": {"cs":"Romans"}
    }

    data = SubjectSchemaV1().load(valid_minimal)
    assert data == valid_minimal

    invalid_no_subject = {
        "identifier": "subj-1",
        "scheme": "no-scheme"
    }
    with pytest.raises(ValidationError):
        data = SubjectSchemaV1().load(invalid_no_subject)


def test_date():
    """Test date schama."""
    valid_full = {
        "start": "2020-06-01",
        "end":  "2021-06-01",
        "description": "Random test date",
        "type": "Other"
    }

    data = DateSchemaV1().load(valid_full)
    assert data == valid_full

    # Note that none start or end are required. But it validates that at
    # least one of them is present.
    valid_minimal = {
        "start": "2020-06-01",
        "type": "Other"
    }

    data = DateSchemaV1().load(valid_minimal)
    assert data == valid_minimal

    invalid_no_type = {
        "start": "2020-06-01",
        "end":  "2021-06-01",
        "description": "Random test date",
    }
    with pytest.raises(ValidationError):
        data = DateSchemaV1().load(invalid_no_type)

    invalid_end_format = {
        "start": "2020/06/01",
        "end":  "2021-06-01",
        "description": "Random test date",
    }
    with pytest.raises(ValidationError):
        data = DateSchemaV1().load(invalid_end_format)

    invalid_end_format = {
        "start": "2020-06-01",
        "end":  "2021-13-01",  # Days and months swaped
        "description": "Random test date",
    }
    with pytest.raises(ValidationError):
        data = DateSchemaV1().load(invalid_end_format)


def test_related_identifiers():
    """Test related identifiers schema."""
    valid_full = {
        "identifier": "10.5281/zenodo.9999988",
        "scheme": "DOI",
        "relation_type": "Requires",
        "resource_type": {
            "type": "image",
            "subtype": "image-photo"
        }
    }

    data = RelatedIdentifierSchemaV1().load(valid_full)
    assert data == valid_full

    valid_minimal = {
        "identifier": "10.5281/zenodo.9999988",
        "scheme": "DOI",
        "relation_type": "Requires"
    }

    data = RelatedIdentifierSchemaV1().load(valid_minimal)
    assert data == valid_minimal

    invalid_no_identifier = {
        "scheme": "DOI",
        "relation_type": "Requires",
        "resource_type": {
            "type": "image",
            "subtype": "image-photo"
        }
    }
    with pytest.raises(ValidationError):
        data = RelatedIdentifierSchemaV1().load(invalid_no_identifier)

    invalid_no_scheme = {
        "identifier": "10.5281/zenodo.9999988",
        "relation_type": "Requires",
        "resource_type": {
            "type": "image",
            "subtype": "image-photo"
        }
    }
    with pytest.raises(ValidationError):
        data = RelatedIdentifierSchemaV1().load(invalid_no_scheme)

    invalid_scheme = {
        "identifier": "10.5281/zenodo.9999988",
        "scheme": "INVALID",
        "relation_type": "Requires",
        "resource_type": {
            "type": "image",
            "subtype": "image-photo"
        }
    }
    with pytest.raises(ValidationError):
        data = RelatedIdentifierSchemaV1().load(invalid_scheme)

    invalid_no_relation_type = {
        "identifier": "10.5281/zenodo.9999988",
        "scheme": "DOI",
        "resource_type": {
            "type": "image",
            "subtype": "image-photo"
        }
    }
    with pytest.raises(ValidationError):
        data = RelatedIdentifierSchemaV1().load(invalid_no_relation_type)

    invalid_relation_type = {
        "identifier": "10.5281/zenodo.9999988",
        "scheme": "DOI",
        "relation_type": "INVALID",
        "resource_type": {
            "type": "image",
            "subtype": "image-photo"
        }
    }
    with pytest.raises(ValidationError):
        data = RelatedIdentifierSchemaV1().load(invalid_relation_type)


def test_references():
    """Test references schema."""
    valid_full = {
        "reference_string": "Reference to something et al.",
        "identifier": "9999.99988",
        "scheme": "GRID"
    }

    data = ReferenceSchemaV1().load(valid_full)
    assert data == valid_full

    valid_minimal = {
        "reference_string": "Reference to something et al."
    }

    data = ReferenceSchemaV1().load(valid_minimal)
    assert data == valid_minimal

    invalid_no_reference = {
        "identifier": "9999.99988",
        "scheme": "GRID"
    }
    with pytest.raises(ValidationError):
        data = ReferenceSchemaV1().load(invalid_no_reference)

    invalid_scheme = {
        "reference_string": "Reference to something et al.",
        "identifier": "9999.99988",
        "scheme": "Invalid"
    }
    with pytest.raises(ValidationError):
        data = ReferenceSchemaV1().load(invalid_scheme)


def test_point():
    """Test point."""
    valid_full = {
        "lat": 41.902604,
        "lon": 12.496189
    }

    data = PointSchemaV1().load(valid_full)
    assert data == valid_full

    invalid_no_lat = {
        "lon": 12.496189
    }
    with pytest.raises(ValidationError):
        data = PointSchemaV1().load(invalid_no_lat)

    invalid_no_lon = {
        "lat": 41.902604,
    }
    with pytest.raises(ValidationError):
        data = PointSchemaV1().load(invalid_no_lon)


def test_location():
    """Test location schema."""
    valid_full = {
        "point": {
            "lat": 41.902604,
            "lon": 12.496189
        },
        "place": "Rome",
        "description": {"cs" : "neco"}
    }

    data = LocationSchemaV1().load(valid_full)
    assert data == valid_full

    valid_minimal = {
        "place": "Rome",
    }

    data = LocationSchemaV1().load(valid_minimal)
    assert data == valid_minimal

    invalid_no_place = {
        "point": {
            "lat": 41.902604,
            "lon": 12.496189
        },
        "description": {"cs" : "neco"}
    }
    with pytest.raises(ValidationError):
        data = LocationSchemaV1().load(invalid_no_place)

    invalid_no_place = {
        "point": {
            "lat": 41.902604,
            "lon": 12.496189
        },
        "description": {"css": "neco"}
    }
    with pytest.raises(ValidationError):
        data = LocationSchemaV1().load(invalid_no_place)

