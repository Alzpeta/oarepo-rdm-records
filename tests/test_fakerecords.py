import marshmallow
import pytest
from marshmallow import ValidationError

from oarepo_rdm_records.cli import create_fake_record
from oarepo_rdm_records.marshmallow.json import MetadataSchemaV1


class MD(MetadataSchemaV1, marshmallow.Schema):
    pass


def test_fake_record():
    pass
    #assert create_fake_record() == MD().load(create_fake_record())