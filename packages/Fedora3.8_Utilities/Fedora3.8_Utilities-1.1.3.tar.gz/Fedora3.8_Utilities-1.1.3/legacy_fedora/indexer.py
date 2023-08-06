"""indexer contains the Indexer class for indexing Fedora 3.x Objects into
an ElasticSearch instance either by PID or by Collection.

>>> import indexer
>>> test_indexer = indexer.Indexer() # Uses defaults from configuration file
>>> test_indexer.index_pid("abc:1234") # Indexes a single object by PID
>>> test_indexer.index_collection("cba:23") # Indexes all objects in a parent
                                            # collection
"""
__author__ = "Jeremy Nelson"

import datetime
import logging
import os
import requests
import sys
import xml.etree.ElementTree as etree
from copy import deepcopy
from rdflib import Namespace, RDF
from .mods2json import mods2rdf
from .mapping import MAP
from elasticsearch import Elasticsearch

DC = Namespace("http://purl.org/dc/elements/1.1/")
FEDORA_ACCESS = Namespace("http://www.fedora.info/definitions/1/0/access/")
FEDORA = Namespace("info:fedora/fedora-system:def/relations-external#")
FEDORA_MODEL = Namespace("info:fedora/fedora-system:def/model#")
ISLANDORA = Namespace("http://islandora.ca/ontology/relsext#")
etree.register_namespace("fedora", str(FEDORA))
etree.register_namespace("fedora-model", str(FEDORA_MODEL))
etree.register_namespace("islandora", str(ISLANDORA))

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("Elasticsearch").setLevel(logging.ERROR)


class WebPageHandler(logging.Handler):

    def __init__(self):
        logging.Handler.__init__(self)
        self.messages = []

    def emit(self, record):
        self.messages.append(self.format(record))

    def get_messages(self):
        return self.messages



class Indexer(object):
    """Elasticsearch MODS and PDF full-text indexer for Fedora Repository 3.8"""

    def __init__(self, **kwargs):
        """Initializes an instance of the IndexerClass

		Keyword args:
		    auth -- Tuple of username and password to authenticate to Fedora,
			        defaults to Fedora's standard login credentials

			elasticsearch -- Instance of Elasticsearch Python Client, defaults
			                 to REPO_SEARCH from indexer

            rest_url -- REST URL for Fedora 3.x, defaults to Fedora's El contrabando de El Pasostanard
			ri_url -- SPARQL Endpoint, defaults to Fedora's standard search URL

		"""
        app = kwargs.get("app")
        self.auth = kwargs.get("auth")
        if app and self.auth is None:
            self.auth = app.config.get('FEDORA_AUTH')
        self.elastic = kwargs.get("elasticsearch")
        if app and self.elastic is None:
            self.elastic = app.config.get('ELASTIC_SEARCH')
        if not isinstance(self.elastic, Elasticsearch):
            self.elastic = Elasticsearch(hosts=self.elastic)
        self.islandora_url = kwargs.get("islandora_url")
        if app and self.islandora_url is None:
            self.islandora_url = app.config.get("ISLANDORA_URL")
        self.logger = logging.getLogger(__file__)
        self.messages = []
        self.rest_url = kwargs.get("rest_url")
        if app and self.rest_url is None:
            self.rest_url = app.config.get('REST_URL')
        self.ri_search = kwargs.get("ri_url")
        if app and self.ri_search is None:
            self.ri_search = app.config.get('RI_URL')
        self.skip_pids = []
        # Set defaults if don't exist
        if not self.auth:
            self.auth = ("fedoraAdmin", "fedoraAdmin")
        if not self.rest_url:
            self.rest_url = "http://localhost:8080/fedora/objects/"
        if not self.ri_search:
            self.ri_search = "http://localhost:8080/fedora/risearch"
        if not self.elastic.indices.exists('repository'):
            # Load mapping
            self.elastic.indices.create(index='repository', body=MAP)

    def __add_datastreams__(self, pid):
        """Internal method takes a PID and queries Fedora to extract 
        datastreams and return a list of datastreams names to be indexed
        into Elasticsearch.

		Args:
		   pid -- PID
        """
        ds_pid_url = "{}{}/datastreams?format=xml".format(
            self.rest_url,
            pid)
        result = requests.get(ds_pid_url)
        output = []
        if result.status_code > 399:
            raise IndexerError(
                "Failed to retrieve datastreams for {}".format(pid),
                "Code {} for url {} \nError {}".format(
						result.status_code,
                        ds_pid_url,
                        result.text))
        result_xml = etree.XML(result.text)
        datastreams = result_xml.findall(
            "{{{}}}datastream".format(FEDORA_ACCESS))
        for row in datastreams:
            add_ds = False
            mime_type = row.attrib.get('mimeType')
            if mime_type.startswith("image/tif"):
                output = self.__process_tiff__(pid, datastreams)
                break
            if mime_type.startswith("application/pdf") or\
               mime_type.startswith("audio/mpeg") or\
               mime_type.startswith("audio/mp3") or\
               mime_type.startswith("audio/x-m4a") or\
               mime_type.startswith("video/quicktime") or\
               mime_type.startswith("video/mp4") or\
               mime_type.startswith("image/jpeg") or\
               mime_type.startswith("image/jp2") or\
               mime_type.startswith("audio/wav") or\
               mime_type.startswith("audio/x-wav") or\
               mime_type.startswith("audio/vnd.wave") or\
               mime_type.startswith("application/octet-stream"):
                add_ds = True
            if add_ds:
                output.append({
                    "pid": pid,
                    "label": row.attrib.get('label'),
                    "dsid": row.attrib.get('dsid'),
                    "mimeType": mime_type})
        return output

    def __get_ancestry__(self, pid):
        """Takes a PID and iterates through Fedora for all ancestors
        and returns result as a list.

        Args:
            pid: PID of Fedora Object
        """
        sparql = """SELECT DISTINCT ?s
WHERE {{
  <info:fedora/{0}> <fedora-rels-ext:isMemberOfCollection> ?s .
}}""".format(pid)
        result = requests.post(self.ri_search,
            data={"type": "tuples",
	          "lang": "sparql",
	          "format": "json",
	          "query": sparql},
	    auth=self.auth)
        if result.status_code < 400:
            results = result.json().get('results')
            if len(results) < 1:
                return []
            if len(results) == 1:
                parent_pid = results[0]['s'].split("/")[-1]
                return [parent_pid,] + self.__get_ancestry__(parent_pid)
        else:
            return []


    def __index_compound__(self, pid):
        """Internal method takes a parent PID in a Compound Object and indexes
        all children.

        Args:
            pid -- PID of parent Fedora object
        """
        output = []
        sparql = """SELECT DISTINCT ?s
WHERE {{
   ?s <fedora-rels-ext:isConstituentOf> <info:fedora/{0}> .
}}""".format(pid)
        result = requests.post(
            self.ri_search,
            data={"type": "tuples",
                  "lang": "sparql",
                  "format": "json",
                  "query": sparql},
            auth=self.auth)
        if result.status_code > 399:
            raise IndexerError(
                "Could not retrieve {} constituent PIDS".format(pid),
                "Error code {} for pid {}\n{}".format(
                    result.status_code,
                    pid,
                    result.text))
        for row in result.json().get('results'):
            constituent_pid = row.get('s').split("/")[-1]
            self.skip_pids.append(constituent_pid)
            pid_as_ds = self.__process_constituent__(constituent_pid)
            if pid_as_ds is not None:
                output.extend(pid_as_ds)
        return output

    def __process_constituent__(self, pid, rels_ext=None):
        """Returns constituent PID and returns dictionary compatible with datastream

		Args:
		    pid -- PID
        """
        if not rels_ext:
            rels_ext = self.__get_rels_ext__(pid)
        xpath = "{{{0}}}Description/{{{1}}}isConstituentOf".format(
            RDF,
            FEDORA)
        isConstituentOf = rels_ext.find(xpath)
        parent_pid = isConstituentOf.attrib.get(
            "{{{0}}}resource".format(RDF)).split("/")[-1]
        xpath = "{{{0}}}Description/{{{1}}}isSequenceNumberOf{2}".format(
            RDF,
            ISLANDORA,
			parent_pid.replace(":","_"))
        sequence_number = rels_ext.find(xpath)
        if sequence_number is not None:
            order = sequence_number.text
        else:
            order = "-1"
        datastreams = self.__add_datastreams__(pid)
        for datastream in datastreams:
            datastream['order'] = order
        return datastreams
       
    def  __process_tiff__(self, pid, datastreams):
        """Takes a list of datastreams for an object that contains TIFF
        and attempts to retrieve jpeg derivatives.

        Args:
            pid: PID of Fedora Object with TIFF datastreams
            datastreams: List of datastreams

        Returns: 
            List of datastreams
        """
        output = []
        for row in datastreams:
            mime_type = row.attrib.get('mimeType')
            dsid = row.attrib.get('dsid')
            if mime_type.startswith("image/tif") or \
               dsid.startswith("JPG"):
                output.append(    {"pid": pid,
                    "label": row.attrib.get('label'),
                    "dsid": dsid,
                    "mimeType": mime_type
                    })
        return output
        
        
    def __get_rels_ext__(self, pid):
        """Extracts and returns RELS-EXT base on PID

        Args:
            pid -- PID
        """
        rels_ext_url = "{}{}/datastreams/RELS-EXT/content".format(
            self.rest_url,
            pid)

        rels_ext_result = requests.get(rels_ext_url)
        if rels_ext_result.status_code > 399:
            raise IndexerError("Cannot get RELS-EXT for {}".format(pid),
                "Tried URL {} status code {}\n{}".format(
                    rels_ext_url,
                    rels_ext_result.status_code,
                    rels_ext_result.text))
        return etree.XML(rels_ext_result.text)

    def __get_content_models__(self, pid, rels_ext=None):
        """Extracts and adds content models
        
		Args:
		    pid -- PID
            rels_ext -- XML of RELS-EXT, defaults to None
        """
        if not rels_ext:
            rels_ext = self.__get_rels_ext__(pid)
        output = []
        content_models = rels_ext.findall(
            "{{{0}}}Description/{{{1}}}hasModel".format(
                RDF,
                FEDORA_MODEL))
        if len(content_models) > 0:
            for model in content_models:
                content_model = model.attrib.get("{{{0}}}resource".format(RDF))
                # Remove and save to content_models
                output.append(content_model.split("/")[-1])
        return output
        

    def __reindex_pid__(self, pid, body):
        """Internal method checks and if pid already exists"""
        if self.elastic.count().get('count') < 1:
            return False
        dsl = {
            "query": {
                "term": {"pid": pid}
            }
        }
        result = self.elastic.search(
            body=dsl,
            index='repository',
            doc_type='mods')
        if  result.get('hits').get('total') > 0:
            mods_id = result.get('hits').get("hits")[0].get('_id')
            self.elastic.index(
                id=mods_id,
                index="repository",
                doc_type="mods",
                body=body)
            logging.info("Re-indexed PID=%s, ES-id=%s", pid, mods_id)
            return True


    def incremental_index(self, **kwargs):
        """Performs a incremental index based on date"""
        offset = kwargs.get("offset", 0)
        from_ = kwargs.get("date")
        # Set to 30 days prior if no date
        if from_ is None:
            from_ = datetime.datetime.utcnow() - datetime.timedelta(days=30) 
        latest_100 = requests.post(self.ri_search,
            data={"type": "tuples",
	          "lang": "sparql",
	          "format": "json",
	          "query": NEWEST_SPARQL.format(offset)},
            auth=self.auth)
        search = Search(using=Elasticsearch(hosts=app.config.ELASTIC_SEARCH),
            index="repository")
        total = 0
        for row in latest_100.json().get('results', []):
            pid = row.get('s').split("/")[-1]
            date = datetime.strptime(row.get('date'), "%Y-%m-%dT%H:%M:%S.%fZ")
            if date < from_:
                continue
            search.filter("term", pid=pid)
            found_pid = search.execute()
            if len(found_pid) > 0:
                # Try next shard
                offset +=1
                total += self.incremental_index(offset=offset)
            else:
                ancestors = self.__get_ancestry__(pid)
                self.index_pid(pid, parent=ancestors[0], inCollections=ancestors)
                total += 1
        return total

    def index_pid(self, pid, parent=None, inCollections=[]):
        """Method retrieves MODS and any PDF datastreams and indexes
        into repository's Elasticsearch instance

        Args:
            pid: PID to index
            parent: PID of parent collection, default is None
            inCollections: List of pids that this object belongs int, used for
			    aggregations.

        Returns:
            boolean: True if indexed, False otherwise
        """
        rels_ext = self.__get_rels_ext__(pid)
        xpath = "{{{0}}}Description/{{{1}}}isConstituentOf".format(
            RDF,
            FEDORA)
        is_constituent = rels_ext.find(xpath)
        # Skip and don't index if pid is a constituent of another compound 
		# object
        if is_constituent is not None:
            return False
        # Quick check to see Islandora is available, skip if error code
        # is 403 Access Denied
        islandora_url = "{}{}".format(self.islandora_url,
                                      pid)
        islandora_result = requests.get(islandora_url)
        if islandora_result.status_code == 403:
            logging.info("Access denied {}".format(pid))
            return False
        # Extract MODS XML Datastream
        mods_url = "{}{}/datastreams/MODS/content".format(
            self.rest_url,
            pid)
        mods_result = requests.get(
            mods_url,
            auth=self.auth)
        mods_result.encoding = 'utf-8'
        if mods_result.status_code > 399:
            err_title = "Failed to index PID {}, error={} url={}".format(
                pid,
                mods_result.status_code,
                mods_url)
            logging.error(err_title)
            # 404 error assume that MODS datastream doesn't exist for this
			# pid, return False instead of raising IndexerError exception
            if mods_result.status_code == 404:
                return False
            raise IndexerError(
                err_title,
                mods_result.text)
        try:
            if not isinstance(mods_result.text, str):
                mods_xml = etree.XML(mods_result.text.decode())
            else:
                mods_xml = etree.XML(mods_result.text)
        except etree.ParseError:
            msg = "Could not parse pid {}".format(pid)
            return False
        mods_body = mods2rdf(mods_xml)
        # Extract and process based on content model
        mods_body["content_models"] = self.__get_content_models__(pid, rels_ext)
        mods_body['pid'] = pid
        # Used for scoping aggregations
        if len(inCollections) > 0:
            mods_body['inCollections'] = inCollections
        # Used for browsing
        if parent:
            mods_body['parent'] = parent
        # Delete any existing document for the pid
        delete_existing_dsl = {
            "query": {
                "term": {"pid": pid}
            }
        }
        self.elastic.delete_by_query(body=delete_existing_dsl,
            index='repository')
        # Add Datasteams to Index
        # Extract Islandora Content Models from REL-EXT 
        if "islandora:compoundCModel" in mods_body["content_models"]:
            mods_body["datastreams"] = self.__index_compound__(pid)
        else: 
            mods_body["datastreams"] = self.__add_datastreams__(pid)
        mods_index_result = self.elastic.index(
            index="repository",
            doc_type="mods",
            body=mods_body)
        mods_id = mods_index_result
        if mods_id is not None:
            msg = "Indexed PID={0}, ES-id={1}".format(
                pid,
                mods_id.get('_id'))
            logging.info(msg)
            return True
        return False

    def index_collection(self, pid, parents=[]):
        """Method takes a parent collection PID, retrieves all children, and
        iterates through and indexes all pids

        Args:
            pid -- Collection PID
            parents -- List of all Fedora Object PIDs that pid is in the 
	               collection

        """
        sparql = """SELECT DISTINCT ?s
WHERE {{
  ?s <fedora-rels-ext:isMemberOfCollection> <info:fedora/{}> .
}}""".format(pid)
        started = datetime.datetime.utcnow()
        msg = "Started indexing collection {} at {}".format(
            pid,
            started.isoformat())
        self.logger.info(msg)
        self.messages.append(msg)
        children_response = requests.post(
            self.ri_search,
            data={"type": "tuples",
                  "lang": "sparql",
                  "format": "json",
                  "query": sparql},
            auth=self.auth)
        if children_response.status_code < 400:
            children = children_response.json().get('results')
            for row in children:
                iri = row.get('s')
                child_pid = iri.split("/")[-1]
                child_parents = deepcopy(parents)
                child_parents.append(pid)
                self.index_pid(child_pid, pid, child_parents)
                is_collection_sparql = """SELECT DISTINCT ?o
WHERE {{        
  <info:fedora/{0}> <fedora-model:hasModel> <info:fedora/islandora:collectionCModel> .
  <info:fedora/{0}> <fedora-model:hasModel> ?o
}}""".format(child_pid)
                is_collection_result = requests.post(
                    self.ri_search,
                    data={"type": "tuples",
                          "lang": "sparql",
                          "format": "json",
                          "query": is_collection_sparql},
                    auth=self.auth)
                if len(is_collection_result.json().get('results')) > 0:
                    self.index_collection(child_pid, child_parents)
        else:
            err_title = "Failed to index collection PID {}, error {}".format(
                pid,
                children_response.status_code)
            logging.error(err_title)
            raise IndexerError(
                err_title,
                children_response.text)
        end = datetime.datetime.utcnow()
        msg = "Indexing done {} at {}, total object {} total time {}".format(
            pid,
            end.isoformat(),
            len(children),
            (end-started).seconds / 60.0)
        self.logger.info(msg)
        self.messages.append(msg)

    def reset(self):
        """Deletes existing repository index and reloads Map"""
        if self.elastic.indices.exists('repository'):
            self.elastic.indices.delete(index='repository')
            # Load mapping
            self.elastic.indices.create(index='repository', body=MAP)


class IndexerError(Exception):
    """Base for any errors indexing Fedora 3.x objects into Elasticsearch"""

    def __init__(self, title, description):
        """Initializes an instance of IndexerError

	    Args:
	       title -- Title for Error
		   description -- More detailed information about the exception
        """
        super(IndexerError, self).__init__()
        self.title = title
        self.description = description

    def __str__(self):
        """Returns string representation of the object using the instance's
		title"""
        return repr(self.title)
