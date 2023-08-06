"""Module repairs errors with MODS metadata"""
__author__ = "Jeremy Nelson, Sarah Bogard"

import datetime
import os
import requests
import sys
import zipfile

import xml.etree.ElementTree as etree
import rdflib
import urllib.parse

MODS = rdflib.Namespace("http://www.loc.gov/mods/v3")
etree.register_namespace("mods", str(MODS))

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

class RepairMODSError(Exception):

    def __init__(self, pid, message):
        self.pid = pid
        self.message = message

    def __str__(self):
        return "Error with {}'s MODS\n{}".format(self.pid, self.message)

def add_mods(**kwargs):
    """Takes a pid and a populated MODS element"""

def update_mods(**kwargs):
    """Function takes pid, field, and old_value, replaces with
	a new_value.

    Args:
        pid -- 
		field_xpath -- 
		old_value -- 
		new_value --
    """
    app = kwargs.get('app')
    pid = kwargs.get("pid")
    field_xpath = kwargs.get("xpath") 
    old_value = kwargs.get("old")
    new_value = kwargs.get("new")
    start = datetime.datetime.utcnow()
    rest_url = kwargs.get("rest_url", app.config.get("REST_URL"))
    auth = kwargs.get("auth", app.config.get("FEDORA_AUTH"))
    mods_base_url = "{}{}/datastreams/MODS".format(
        rest_url,
        pid.strip())
    get_mods_url = "{}/content".format(mods_base_url)
    mods_result = requests.get(
        get_mods_url,
        auth=auth)
    if mods_result.status_code > 399:
        err_title = """"Failed to replace {} with {} for PID {}, 
error={} url={}""".format(
            old_value, 
            new_value, 
            pid,
            mods_result.status_code,
            get_mods_url)
    raw_xml = mods_result.text
    mods_xml = etree.XML(raw_xml)
    old_value_elements = mods_xml.findall(field_xpath, {"mods": str(MODS)})
    for element in old_value_elements:
        if element.text == old_value:
            element.text = new_value
    url_params = {"controlGroup": "M",
        "dsLabel": "MODS",
        "mimeType": "text/xml",
        "versionable": "true"}
    mods_update_url = "{}?{}".format(
        mods_base_url,
        urllib.parse.urlencode(url_params))
    raw_xml = etree.tostring(mods_xml)
    put_result = requests.post(
        mods_update_url,
	files={"content":  raw_xml},
        auth=app.config.get('FEDORA_AUTH'))
    if put_result.status_code < 300:
        return True
    else:
        raise RepairMODSError(
            pid, 
            "Failed to update MODS with PUT\nStatus code {}\n{}".format(
                put_result.status_code,
                put_result.text))

def update_multiple(**kwargs):
    """Function takes a list of PIDs, the MODS field xpath, the old value to be 
    replaced by the new value.

    Keyword args:
        pid_list -- Listing of PIDs
        field_xpath -- Field XPath
        old_value -- Old string value to be replaced
        new_value -- New string value
    """
    app = kwargs.get('app')
    pid_list = kwargs.get('pid_list')
    field_xpath = kwargs.get('xpath')
    old_value = kwargs.get('old_value')
    new_value = kwargs.get('new_value') 
    start = datetime.datetime.utcnow()
    msg = "Starting MODS update for {} PIDS at {}".format(
        len(pid_list), 
        start.isoformat())
    yield msg
    errors = []
    for i, pid in enumerate(pid_list):
        if not update_mods(pid, field_xpath, old_value, new_value):
            errors.append(pid)
        if not i%25:
            #print(i, end="")
            yield i
        elif not i%10:
            #print(".", end="")
            yield "."
    end = datetime.datetime.utcnow()
    msg = "Finished updating MODS for {}, errors {} at {}, total {}".format(
        len(pid_list),
        len(errors),
        end.isoformat(),
        (end-start).seconds / 60.0)
    yield msg


def get_collection_pids(config, pid):
    """Function takes a Flask app config and a collection PID,
    returns all children PIDS

    Args:
        config: Flask app config
        pid: PID of collection
    """
    output = []
    sparql = """SELECT DISTINCT ?s
WHERE {{
  ?s <fedora-rels-ext:isMemberOfCollection> <info:fedora/{}> .
}}""".format(pid)
    children_response = requests.post(
            config.get("RI_SEARCH"),
            data={"type": "tuples",
                  "lang": "sparql",
                  "format": "json",
                  "query": sparql},
            auth=config.get("FEDORA_AUTH"))
    children = children_response.json().get('results')
    for row in children:
        iri = row.get('s')
        child_pid = iri.split("/")[-1]
        output.append(child_pid)
    return output
