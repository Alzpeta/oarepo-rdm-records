import json

import pytest
from jsonschema import ValidationError

# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# Invenio OpenID Connect is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


def get_schema():
    """This function loads the given schema available"""

    try:
        with open('test_module/jsonschemas/test/test-v1.0.0.json', 'r') as file:
            schema = json.load(file)
    except:
        with open('./tests/test_module/jsonschemas/test/test-v1.0.0.json', 'r') as file:
            schema = json.load(file)

    return schema


def get_mapping():
    """This function loads the given schema available"""

    try:
        with open('test_module/mappings/v7/test/test-v1.0.0.json', 'r') as file:
            mapping = json.load(file)
    except:
        with open('./tests/test_module/mappings/v7/test/test-v1.0.0.json', 'r') as file:
            mapping = json.load(file)

    return mapping


def test_json(app):
    """Test of json schema with app."""
    schema = app.extensions['invenio-records']

    data = json.loads('{"these": {"titles" : {"cs": "jej", "en": "yay"}}}')
    schema.validate(data, get_schema())

    data = json.loads('{"these": {"subjects":[{"subject": {"cs":"neco", "en-us":"neco jinyho"}}]}}')
    schema.validate(data, get_schema())

    data = json.loads('{"these": {"locations":[{"description": {"cs":"neco", "en-us":"neco jinyho"}, "place": "string"}]}}')
    schema.validate(data, get_schema())

    data = json.loads('{"these": {"titles" : {"css": "jej", "en": "yay"}}}')
    with pytest.raises(ValidationError):
        schema.validate(data, get_schema())


def test_mapping(app):
    data = get_mapping()
    assert data == {
        "mappings": {
            "properties": {
                "RDMRecord": {
                    "date_detection": False,
                    "numeric_detection": False,
                    "properties": {
                        "_access": {
                            "type": "object",
                            "properties": {
                                "metadata_restricted": {
                                    "type": "boolean"
                                },
                                "files_restricted": {
                                    "type": "boolean"
                                }
                            }
                        },
                        "_bucket": {
                            "enabled": False
                        },
                        "_conceptrecid": {
                            "type": "keyword"
                        },
                        "_created_by": {
                            "type": "integer"
                        },
                        "_default_preview": {
                            "enabled": False
                        },
                        "_files": {
                            "type": "object",
                            "properties": {
                                "bucket": {
                                    "type": "keyword"
                                },
                                "key": {
                                    "type": "keyword",
                                    "copy_to": "filename"
                                },
                                "version_id": {
                                    "type": "keyword"
                                },
                                "size": {
                                    "type": "long"
                                },
                                "checksum": {
                                    "type": "keyword"
                                },
                                "previewer": {
                                    "type": "keyword"
                                },
                                "type": {
                                    "type": "keyword",
                                    "copy_to": "filetype"
                                }
                            }
                        },
                        "_internal_notes": {
                            "type": "object",
                            "properties": {
                                "user": {
                                    "type": "keyword"
                                },
                                "note": {
                                    "type": "text"
                                },
                                "timestamp": {
                                    "type": "date"
                                }
                            }
                        },
                        "_recid": {
                            "type": "keyword"
                        },
                        "_oai": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "keyword"
                                },
                                "sets": {
                                    "type": "keyword"
                                },
                                "updated": {
                                    "type": "date"
                                }
                            }
                        },
                        "_owners": {
                            "type": "integer"
                        },
                        "_embargo_date": {
                            "type": "date"
                        },
                        "_contact": {
                            "type": "keyword"
                        },
                        "_communities": {
                            "type": "object",
                            "properties": {
                                "accepted": {
                                    "type": "object",
                                    "properties": {
                                        "id": {
                                            "type": "keyword"
                                        },
                                        "comid": {
                                            "type": "keyword"
                                        },
                                        "title": {
                                            "type": "text"
                                        },
                                        "request_id": {
                                            "type": "keyword"
                                        },
                                        "created_by": {
                                            "type": "integer"
                                        }
                                    }
                                },
                                "pending": {
                                    "type": "object",
                                    "properties": {
                                        "id": {
                                            "type": "keyword"
                                        },
                                        "comid": {
                                            "type": "keyword"
                                        },
                                        "title": {
                                            "type": "text"
                                        },
                                        "request_id": {
                                            "type": "keyword"
                                        },
                                        "created_by": {
                                            "type": "integer"
                                        }
                                    }
                                },
                                "rejected": {
                                    "type": "object",
                                    "properties": {
                                        "id": {
                                            "type": "keyword"
                                        },
                                        "comid": {
                                            "type": "keyword"
                                        },
                                        "title": {
                                            "type": "text"
                                        },
                                        "request_id": {
                                            "type": "keyword"
                                        },
                                        "created_by": {
                                            "type": "integer"
                                        }
                                    }
                                }
                            }
                        },
                        "access_right": {
                            "type": "keyword"
                        },
                        "resource_type": {
                            "type": "object",
                            "properties": {
                                "type": {
                                    "type": "keyword"
                                },
                                "subtype": {
                                    "type": "keyword"
                                }
                            }
                        },
                        "identifiers": {
                            "type": "object"
                        },
                        "creators": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "text"
                                },
                                "type": {
                                    "type": "keyword"
                                },
                                "given_name": {
                                    "type": "text"
                                },
                                "family_name": {
                                    "type": "text"
                                },
                                "identifiers": {
                                    "type": "object"
                                },
                                "affiliations": {
                                    "type": "object",
                                    "properties": {
                                        "name": {
                                            "type": "text"
                                        },
                                        "identifiers": {
                                            "type": "object"
                                        }
                                    }
                                }
                            }
                        },
                        "titles": {"type": "multilingual"},
                        "subjects": {"type": "multilingual"},
                        "contributors": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "text"
                                },
                                "type": {
                                    "type": "keyword"
                                },
                                "given_name": {
                                    "type": "text"
                                },
                                "family_name": {
                                    "type": "text"
                                },
                                "identifiers": {
                                    "type": "object"
                                },
                                "affiliations": {
                                    "type": "object",
                                    "properties": {
                                        "name": {
                                            "type": "text"
                                        },
                                        "identifiers": {
                                            "type": "object"
                                        }
                                    }
                                },
                                "role": {
                                    "type": "keyword"
                                }
                            }
                        },
                        "dates": {
                            "type": "object",
                            "properties": {
                                "start": {
                                    "type": "date"
                                },
                                "end": {
                                    "type": "date"
                                },
                                "type": {
                                    "type": "keyword"
                                },
                                "description": {
                                    "type": "text"
                                }
                            }
                        },
                        "language": {
                            "type": "keyword"
                        },
                        "related_identifiers": {
                            "type": "object",
                            "properties": {
                                "identifier": {
                                    "type": "keyword",
                                    "copy_to": "related.identifier"
                                },
                                "scheme": {
                                    "type": "keyword"
                                },
                                "relation_type": {
                                    "type": "keyword"
                                },
                                "resource_type": {
                                    "properties": {
                                        "subtype": {
                                            "type": "keyword"
                                        },
                                        "type": {
                                            "type": "keyword"
                                        }
                                    }
                                }
                            }
                        },
                        "version": {
                            "type": "keyword"
                        },
                        "licenses": {
                            "type": "object",
                            "properties": {
                                "license": {"type": "multilingual"},
                                "uri": {
                                    "type": "keyword"
                                },
                                "identifier": {
                                    "type": "keyword"
                                },
                                "scheme": {
                                    "type": "keyword"
                                }
                            }
                        },
                        "descriptions": {"type": "multilingual"},
                        "locations": {
                            "type": "object",
                            "properties": {
                                "place": {
                                    "type": "text"
                                },
                                "description": {"type": "multilingual"},
                                "point": {
                                    "type": "object",
                                    "properties": {
                                        "lat": {
                                            "type": "double"
                                        },
                                        "lon": {
                                            "type": "double"
                                        }
                                    }
                                }
                            }
                        },
                        "references": {
                            "type": "object",
                            "properties": {
                                "reference_string": {
                                    "type": "text"
                                },
                                "identifier": {
                                    "type": "keyword"
                                },
                                "scheme": {
                                    "type": "keyword"
                                }
                            }
                        },
                        "_created": {
                            "type": "date"
                        },
                        "_updated": {
                            "type": "date"
                        },
                        "$schema": {
                            "type": "keyword",
                            "index": False
                        },
                        "extensions": {
                            "type": "object",
                            "dynamic": False,
                            "enabled": False
                        },
                        "extensions_keywords": {
                            "type": "object",
                            "properties": {
                                "key": {"type": "keyword"},
                                "value": {"type": "keyword"}
                            }
                        },
                        "extensions_texts": {
                            "type": "object",
                            "properties": {
                                "key": {"type": "keyword"},
                                "value": {"type": "text"}
                            }
                        },
                        "extensions_longs": {
                            "type": "object",
                            "properties": {
                                "key": {"type": "keyword"},
                                "value": {"type": "long"}
                            }
                        },
                        "extensions_dates": {
                            "type": "object",
                            "properties": {
                                "key": {"type": "keyword"},
                                "value": {"type": "date"}
                            }
                        },
                        "extensions_booleans": {
                            "type": "object",
                            "properties": {
                                "key": {"type": "keyword"},
                                "value": {"type": "boolean"}
                            }
                        }
                    }
                }
            }
        }
    }