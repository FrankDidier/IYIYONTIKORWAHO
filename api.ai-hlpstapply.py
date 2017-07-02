from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import jsonpath

from flask import Flask
from flask import request
from flask import make_response


# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    if req.get("result").get("action") != "Bachapp":
        return {}
    if req.get("result").get("action") != "Mastapp":
        return {}
    if req.get("result").get("action") != "Phdapp":
        return {}
    if req.get("result").get("action") != "Nondapp":
        return {}

    with open('Sheet1.json') as f:
        data = f.read()
        jsondata = json.loads(data)
    # data = json.loads(result)
    res = makeWebhookResult(jsondata)
    return res

def makejsonQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    Levp = parameters.get("Level")
    Progr = parameters.get("ProgramName")
    time = parameters.get("StartDate")
    if Levp is None:
        return None
    elif Progr is None:
        return None
    elif time is None:
        return None

    match = jsonpath.jsonpath(jsondata,'$.features[[?(@.ProgramName == Progr && @.Level == Levp && @.StartDate == time)]].UniversityName,Program URL,Years,App Deadline,1stYrTuition,Tuition')
    return match


def makeWebhookResult(data):
    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    if result is None:
        return {}

    channel = result.get('channel')
    if channel is None:
        return {}

    Univname = channel.get('UniversityName')
    progname = channel.get('ProgramName')
    progurl = channel.get('Program URL')
    yaz = channel.get('Years')
    Appdead = channel.get('App Deadline')
    FirstTuit = channel.get('1stYrTuition')
    Tuit = channel.get('Tuition')

    if (progname is None) or (progurl is None) or (yaz is None) or (Appdead is None) or (FirstTuit is None) or (Univname is None) or (Tuit is None):
        return {}


    speech = "Would you like to study in " + Univname.get('UniversityName') + ": " + progname.get('ProgramName') + \
             ", click this link to apply to this program " + progurl.get('Program URL') + "With Application Deadline on " + Appdead.get('Tuition') + \
             ",Whereby First Year Tuition fees is " + FirstTuit.get('1stYrTuition') + "In total Tuition Fees is " + Tuit.get('Tuition') + \
             ",this program will take " + yaz.get('Years') + "Years"

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        #"contexts": [],
        "source": "agent"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
