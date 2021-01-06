# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2020 CERN.
# Copyright (C) 2019-2020 Northwestern University.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Tests for Invenio RDM Records JSON Schemas."""

import pytest
from marshmallow import ValidationError
from oarepo_rdm_records.marshmallow import (
    AffiliationSchema, CreatorSchema, ReferenceSchema, RelatedIdentifierSchema, DateSchema, RightsSchema,
    ContributorSchema
)


def test_affiliations():
    """Test affiliations schema."""
    valid_full = {
        "name": "Entity One",
        "identifiers": {
            "ror": "03yrm5c26"
        }
    }
    data = AffiliationSchema().load(valid_full)
    assert data == valid_full

    invalid_no_name = {
        "identifiers": {
            "ror": "03yrm5c26"
        }
    }
    with pytest.raises(ValidationError):
        data = AffiliationSchema().load(invalid_no_name)

    invalid_identifier = {
        "name": "Entity One",
        "identifiers": {
            "ror": ""
        }
    }
    with pytest.raises(ValidationError):
        data = AffiliationSchema().load(invalid_identifier)

    invalid_scheme = {
        "name": "Entity One",
        "identifiers": {
            "": "03yrm5c26"
        }
    }
    with pytest.raises(ValidationError):
        data = AffiliationSchema().load(invalid_scheme)


def test_creator():
    """Test creator schema."""
    # If present, bare minimum
    valid_minimal = {
        "given_name": "Julius",
        "family_name": "Caesar",
        "name": "Caesar, Julius",
        "type": "personal"
    }
    data = CreatorSchema().load(valid_minimal)
    assert data == valid_minimal

    # Full person
    valid_full_person = {
        "name": "Caesar, Julius",
        "type": "personal",
        "given_name": "Julius",
        "family_name": "Caesar",
        "identifiers": {
            "orcid": '0000-0002-1825-0097',
        },
        "affiliations": [{
            "name": "Entity One",
            "identifiers": {
                "ror": "03yrm5c26"
            }
        }]
    }
    data = CreatorSchema().load(valid_full_person)
    assert data == valid_full_person

    # Full organization
    valid_full_org = {
        "name": "California Digital Library",
        "type": "organizational",
        "identifiers": {
            "ror": "03yrm5c26",
        }
    }
    data = CreatorSchema().load(valid_full_org)
    assert data == valid_full_org

    invalid_no_name = {
        "type": "Personal",
        "given_name": "Julio",
        "family_name": "Cesar",
        "identifiers": {
            "orcid": "0000-0002-1825-0097",
        },
        "affiliations": [{
            "name": "Entity One",
            "identifiers": {
                "ror": "03yrm5c26"
            }
        }]
    }
    with pytest.raises(ValidationError):
        data = CreatorSchema().load(invalid_no_name)

    invalid_no_type = {
        "name": "Julio Cesar",
    }
    with pytest.raises(ValidationError):
        data = CreatorSchema().load(invalid_no_type)

    invalid_type = {
        "name": "Julio Cesar",
        "type": "Invalid",
    }
    with pytest.raises(ValidationError):
        data = CreatorSchema().load(invalid_type)

    invalid_scheme = {
        "name": "Julio Cesar",
        "type": "personal",
        "identifiers": {
            "unapproved scheme": "0000-0002-1825-0097",
        }
    }
    with pytest.raises(ValidationError):
        data = CreatorSchema().load(invalid_type)

    invalid_orcid_identifier = {
        "name": "Julio Cesar",
        "type": "personal",
        "identifiers": {
            # NOTE: This *is* an invalid ORCiD
            "Orcid": "9999-9999-9999-9999",
        }
    }
    with pytest.raises(ValidationError):
        data = CreatorSchema().load(invalid_orcid_identifier)

    invalid_ror_identifier = {
        "name": "Julio Cesar Empire",
        "type": "organizational",
        "identifiers": {
            "ror": "9999-9999-9999-9999",
        }
    }
    with pytest.raises(ValidationError):
        data = CreatorSchema().load(invalid_ror_identifier)

    invalid_identifier_for_person = {
        "name": "Julio Cesar",
        "type": "personal",
        "identifiers": {
            "ror": "03yrm5c26"
        }
    }
    with pytest.raises(ValidationError):
        data = CreatorSchema().load(invalid_identifier_for_person)

    invalid_identifier_for_org = {
        "name": "Julio Cesar Empire",
        "type": "organizational",
        "identifiers": {
            "Orcid": "0000-0002-1825-0097",
        }
    }
    with pytest.raises(ValidationError):
        data = CreatorSchema().load(invalid_identifier_for_org)


def test_contributor():
    """Test contributor schema."""
    valid_full = {
        "name": "Caesar, Julius",
        "type": "personal",
        "given_name": "Julius",
        "family_name": "Caesar",
        "identifiers": {
            "orcid": "0000-0002-1825-0097",
        },
        "affiliations": [{
            "name": "Entity One",
            "identifiers": {
                "ror": "03yrm5c26"
            }
        }],
        "role": "RightsHolder"
    }

    data = ContributorSchema().load(valid_full)
    assert data == valid_full

    valid_minimal = {
        "given_name": "Julius",
        "family_name": "Caesar",
        "name": "Caesar, Julius",
        "type": "personal",
        "role": "RightsHolder"
    }

    data = ContributorSchema().load(valid_minimal)
    assert data == valid_minimal

    invalid_no_name = {
        "type": "personal",
        "given_name": "Julius",
        "family_name": "Caesar",
        "identifiers": {
            "Orcid": "0000-0002-1825-0097",
        },
        "role": "RightsHolder"
    }
    with pytest.raises(ValidationError):
        data = ContributorSchema().load(invalid_no_name)

    invalid_no_name_type = {

        "name": "Caesar, Julius",
        "given_name": "Julius",
        "family_name": "Caesar",
        "identifiers": {
            "Orcid": "0000-0002-1825-0097",
        },
        "role": "RightsHolder"
    }
    with pytest.raises(ValidationError):
        data = ContributorSchema().load(invalid_no_name_type)

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
        data = ContributorSchema().load(invalid_name_type)

    invalid_no_role = {
        "name": "Julio Cesar",
        "type": "personal",
        "given_name": "Julio",
        "family_name": "Cesar",
        "identifiers": {
            "Orcid": "0000-0002-1825-0097",
        },
    }
    with pytest.raises(ValidationError):
        data = ContributorSchema().load(invalid_no_role)


def test_license():
    """Test license scehma."""
    valid_full = {
        "rights": "Copyright Maximo Decimo Meridio 2020. Long statement",
        "uri": "https://opensource.org/licenses/BSD-3-Clause",
        "identifier": "BSD-3",
        "scheme": "BSD-3"
    }

    data = RightsSchema().load(valid_full)
    assert data == valid_full

    valid_minimal = {
        "rights": "Copyright Maximo Decimo Meridio 2020. Long statement"
    }

    data = RightsSchema().load(valid_minimal)
    assert data == valid_minimal

    invalid_no_license = {
        "uri": "https://opensource.org/licenses/BSD-3-Clause",
        "identifier": "BSD-3",
        "scheme": "BSD-3"
    }
    with pytest.raises(ValidationError):
        data = RightsSchema().load(invalid_no_license)


def test_date():
    """Test date schama."""
    valid_full = {
        "date": "2020-06-01",
        "description": "Random test date",
        "type": "other"
    }

    data = DateSchema().load(valid_full)
    assert data == valid_full

    # Note that none start or end are required. But it validates that at
    # least one of them is present.
    valid_minimal = {
        "date": "2020-06-01",
        "type": "other"
    }

    data = DateSchema().load(valid_minimal)
    assert data == valid_minimal

    invalid_no_type = {
        "date": "2020-06-01",
        "description": "Random test date",
    }
    with pytest.raises(ValidationError):
        data = DateSchema().load(invalid_no_type)

    invalid_end_format = {
        "date": "2021-06-01",
        "description": "Random test date",
    }
    with pytest.raises(ValidationError):
        data = DateSchema().load(invalid_end_format)

    invalid_end_format = {
        "date": "2021-13-01",  # Days and months swaped
        "description": "Random test date",
    }
    with pytest.raises(ValidationError):
        data = DateSchema().load(invalid_end_format)


def test_related_identifiers():
    """Test related identifiers schema."""
    valid_full = {
        "identifier": "10.5281/zenodo.9999988",
        "scheme": "doi",
        "relation_type": "requires",
        "resource_type": {
            "type": "image",
            "subtype": "image-photo"
        }
    }

    data = RelatedIdentifierSchema().load(valid_full)
    assert data == valid_full

    valid_minimal = {
        "identifier": "10.5281/zenodo.9999988",
        "scheme": "doi",
        "relation_type": "requires"
    }

    data = RelatedIdentifierSchema().load(valid_minimal)
    assert data == valid_minimal

    invalid_no_identifier = {
        "scheme": "doi",
        "relation_type": "requires",
        "resource_type": {
            "type": "image",
            "subtype": "image-photo"
        }
    }
    with pytest.raises(ValidationError):
        data = RelatedIdentifierSchema().load(invalid_no_identifier)

    invalid_no_scheme = {
        "identifier": "10.5281/zenodo.9999988",
        "relation_type": "requires",
        "resource_type": {
            "type": "image",
            "subtype": "image-photo"
        }
    }
    with pytest.raises(ValidationError):
        data = RelatedIdentifierSchema().load(invalid_no_scheme)

    invalid_scheme = {
        "identifier": "10.5281/zenodo.9999988",
        "scheme": "INVALID",
        "relation_type": "requires",
        "resource_type": {
            "type": "image",
            "subtype": "image-photo"
        }
    }
    with pytest.raises(ValidationError):
        data = RelatedIdentifierSchema().load(invalid_scheme)

    invalid_no_relation_type = {
        "identifier": "10.5281/zenodo.9999988",
        "scheme": "doi",
        "resource_type": {
            "type": "image",
            "subtype": "image-photo"
        }
    }
    with pytest.raises(ValidationError):
        data = RelatedIdentifierSchema().load(invalid_no_relation_type)

    invalid_relation_type = {
        "identifier": "10.5281/zenodo.9999988",
        "scheme": "doi",
        "relation_type": "INVALID",
        "resource_type": {
            "type": "image",
            "subtype": "image-photo"
        }
    }
    with pytest.raises(ValidationError):
        data = RelatedIdentifierSchema().load(invalid_relation_type)


def test_references():
    """Test references schema."""
    valid_full = {
        "reference": "Reference to something et al.",
        "identifier": "9999.99988",
        "scheme": "grid"
    }

    data = ReferenceSchema().load(valid_full)
    assert data == valid_full

    valid_minimal = {
        "reference": "Reference to something et al."
    }

    data = ReferenceSchema().load(valid_minimal)
    assert data == valid_minimal

    invalid_no_reference = {
        "identifier": "9999.99988",
        "scheme": "grid"
    }
    with pytest.raises(ValidationError):
        data = ReferenceSchema().load(invalid_no_reference)

    invalid_scheme = {
        "reference": "Reference to something et al.",
        "identifier": "9999.99988",
        "scheme": "invalid"
    }
    with pytest.raises(ValidationError):
        data = ReferenceSchema().load(invalid_scheme)
