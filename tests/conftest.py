# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# Invenio OpenID Connect is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Common pytest fixtures and plugins."""

from __future__ import absolute_import, print_function

import os
import shutil
import sys
import tempfile
from pathlib import Path

import pytest
from flask import Flask
from invenio_base.signals import app_loaded
from invenio_db import InvenioDB, db as db_
from invenio_indexer import InvenioIndexer
from invenio_jsonschemas import InvenioJSONSchemas
from invenio_pidstore import InvenioPIDStore
from invenio_records import InvenioRecords
from invenio_search import InvenioSearch
from oarepo_mapping_includes.ext import OARepoMappingIncludesExt
from oarepo_references import OARepoReferences
from oarepo_taxonomies.cli import init_db, import_taxonomy
from oarepo_taxonomies.ext import OarepoTaxonomies
from sqlalchemy_utils import database_exists, drop_database, create_database


@pytest.yield_fixture(scope="module")
def app(request):
    """Test mdcobject."""
    instance_path = tempfile.mkdtemp()
    app = Flask('testapp', instance_path=instance_path)

    app.config.update(
        ACCOUNTS_JWT_ENABLE=False,
        INDEXER_DEFAULT_DOC_TYPE='record-v1.0.0',
        RECORDS_REST_ENDPOINTS={},
        RECORDS_REST_DEFAULT_CREATE_PERMISSION_FACTORY=None,
        RECORDS_REST_DEFAULT_DELETE_PERMISSION_FACTORY=None,
        RECORDS_REST_DEFAULT_READ_PERMISSION_FACTORY=None,
        RECORDS_REST_DEFAULT_UPDATE_PERMISSION_FACTORY=None,
        SERVER_NAME='localhost:5000',
        JSONSCHEMAS_HOST='localhost:5000',
        CELERY_ALWAYS_EAGER=True,
        CELERY_RESULT_BACKEND='cache',
        CELERY_CACHE_BACKEND='memory',
        FLASK_TAXONOMIES_URL_PREFIX='/2.0/taxonomies/',
        CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            'SQLALCHEMY_DATABASE_URI', 'sqlite:///test.db'
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        SUPPORTED_LANGUAGES=["cs", "en"],
        TESTING=True,
        ELASTICSEARCH_DEFAULT_LANGUAGE_TEMPLATE={
            "type": "text",
            "fields": {
                "keywords": {
                    "type": "keyword"
                }
            }
        }
    )

    app.secret_key = 'changeme'

    InvenioDB(app)
    OarepoTaxonomies(app)
    OARepoReferences(app)
    InvenioRecords(app)
    InvenioJSONSchemas(app)
    InvenioPIDStore(app)
    InvenioSearch(app)
    InvenioIndexer(app)
    OARepoMappingIncludesExt(app)

    #
    app_loaded.send(app, app=app)

    with app.app_context():
        yield app

    # Teardown instance path.
    shutil.rmtree(instance_path)


@pytest.fixture(scope="module")
def db(app):
    """Create database for the tests."""
    dir_path = os.path.dirname(__file__)
    parent_path = str(Path(dir_path).parent)
    db_path = os.environ.get('SQLALCHEMY_DATABASE_URI', f'sqlite:////{parent_path}/database.db')
    os.environ["INVENIO_SQLALCHEMY_DATABASE_URI"] = db_path
    app.config.update(
        SQLALCHEMY_DATABASE_URI=db_path
    )
    if database_exists(str(db_.engine.url)):
        drop_database(db_.engine.url)
    if not database_exists(str(db_.engine.url)):
        create_database(db_.engine.url)
    db_.create_all()
    # subprocess.run(["invenio", "taxonomies", "init"])
    runner = app.test_cli_runner()
    result = runner.invoke(init_db)
    if result.exit_code:
        print(result.output, file=sys.stderr)
    assert result.exit_code == 0

    for f in os.listdir('taxonomies'):
        result = runner.invoke(import_taxonomy, os.path.join('taxonomies', f))
        if result.exit_code:
            print(result.output, file=sys.stderr)
        assert result.exit_code == 0
    yield db_

    # Explicitly close DB connection
    db_.session.close()
    db_.drop_all()
