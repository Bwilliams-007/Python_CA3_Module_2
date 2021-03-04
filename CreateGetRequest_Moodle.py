from requests import get, post
import json
from datetime import datetime
from dateutil.parser import parse
import os
import re
from bs4 import BeautifulSoup

KEY = "8cc87cf406775101c2df87b07b3a170d"
URL = "https://034f8a1dcb5c.eu.ngrok.io"
ENDPOINT = "/webservice/rest/server.php"


def rest_api_parameters(in_args, prefix='', out_dict=None):
    if out_dict == None:
        out_dict = {}
    if not type(in_args) in (list, dict):
        out_dict[prefix] = in_args
        return out_dict
    if prefix == '':
        prefix = prefix + '{0}'
    else:
        prefix = prefix + '[{0}]'
    if type(in_args) == list:
        for idx, item in enumerate(in_args):
            rest_api_parameters(item, prefix.format(idx), out_dict)
    elif type(in_args) == dict:
        for key, item in in_args.items():
            rest_api_parameters(item, prefix.format(key), out_dict)
    return out_dict


def call(fname, **kwargs):
    parameters = rest_api_parameters(kwargs)
    parameters.update({"wstoken": KEY, 'moodlewsrestformat': 'json', "wsfunction": fname})
    # print(parameters)
    response = post(URL + ENDPOINT, data=parameters).json()
    if type(response) == dict and response.get('exception'):
        raise SystemError("Error calling Moodle API\n", response)
    return response


################################################
# Rest-Api classes
################################################

class LocalGetSections(object):
    """Get settings of sections. Requires courseid. Optional you can specify sections via number or id."""

    def __init__(self, cid, secnums=[], secids=[]):
        self.getsections = call('local_wsmanagesections_get_sections', courseid=cid, sectionnumbers=secnums,
                                sectionids=secids)


courseid = "28"  # Exchange with valid id.
# Get all sections of the course.
sec = LocalGetSections(courseid)

grid_col = sec.getsections

json_object = json.dumps(grid_col, indent=4, sort_keys=True)

json_object1 = json.loads(json_object)

for key in json_object1:
    print(json_object1)
    for i in range(len(json_object1)):
        print(i)

        valuedate = json_object1[i]["name"]
        if "-" in valuedate:
            valuespit = valuedate.split("-")
            valuespitleft = valuespit[0]
            valuespitright = valuespit[1]
            currentyear = datetime.now().year
            onverTodatelift = parse("{}, {}".format(valuespitleft, currentyear))
            onverTodateright = parse("{}, {}".format(valuespitright, currentyear))
            print(onverTodatelift)
            print(onverTodateright)

        valuelink = json_object1[i]["summary"]
        print("link i summary: "+valuelink)
        directory = (
            r"C:\Users\ThinkPad T440\Documents\Course_work_Al_ML\Module_2\Python_Class\Python_CA_Module_2\Semaster1")

        for folder, sub_folders, files in os.walk(directory):
            for sub_fold in sub_folders:
                print("\t Subfolder: "+sub_fold)


