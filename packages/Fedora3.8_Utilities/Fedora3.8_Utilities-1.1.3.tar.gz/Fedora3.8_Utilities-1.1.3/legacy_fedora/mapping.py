"""Elasticsearch Mapping for DACC Repository"""
__author__ = "Jeremy Nelson"

MAP = {"mappings": {
    "mods": {
        "properties": {
            "abstract": {
                "type": "text"
            },
            "adminNote": {
                "type": "text"
            },
            "content_models": {
              "index": "false",
                       "type": "text"
            },
            "contributor": {
                "type": "text"
            },
            "creator": {
                "type": "text"
            },
            "datastreams": {
               "properties": {
                       "dsid": {
                           "index": "false",
                           "type": "text"
                       },
					   "label": {
                           "index": "false",
                           "type": "text"
                       },
                       "mimeType": {
                           "index": "false",
                           "type": "text"
                       }
                }
            },
            "dateCreated": {
               "index": "false",
                "type": "text"
            },
            "dateIssued": {
                "type": "text"
            },
            "datePublished": {
                "index": "false",
                "type": "text"
	    },
            "degreeGrantor": {
                "type": "text"
            },
            "degreeName": {
                "type": "text"
            },
            "degreeType": {
                "type": "text"
            },
            "digitalOrigin": {
                "type": "text"
            },
            "extent": {
                "type": "text"
            },
            "genre": {
                "index": "false",
                "type": "text"
            },
            "handle": {
                "type": "text"
            },
            "inCollections": {
                "index": "false",
                "type": "text"
            },
            "language": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type":"keyword"
                    }
                }
            },
            "note": {
                "type": "text"
            },
            "parent": {
                "index": "false",
                "type": "text"
            },
            "photographer": {
                "type": "text"
            },

            "pid": {
                "index": "false",
                "type": "text"
            },
            "place": {
                "type": "text"
            },
            "publisher": {
                "type": "text"
            },
            "publicationYear": {             
                "index": "false",
                "type": "text"
            },
            "sponsor": {
                "type": "text"
            },
            "subject": {
                "properties": {
                    "genre": {
			"index": "false",
                        "type": "text"
                    },
                    "geographic": {
		        "index": "false",
                        "type": "text"
                    },
                    "temporal": {
		        "index": "false",
                        "type": "text"
                    },
                    "topic": {
			"index": "false",
                        "type": "text"
                    }
                }
            },
            "thesis": {
                "type": "text"
            },
            "thesisAdvisor": {
                "type": "text"
            },
            "titleAlternative": {
                "type": "text"
            },
            "titlePrincipal": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }

            },
            "titleRaw": {
                "type": "text",
                "index": "false"
            },
            "typeOfResource": {
                "index": "false",
                "type": "text"
            },
            "useAndReproduction": {
                "type": "text"
            }
            }
        }
    }
}
