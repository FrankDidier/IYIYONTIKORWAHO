#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()


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
    #elif req.get("result").get("action") != "Mastapp":
    #   return {}
    #elif req.get("result").get("action") != "Phdapp":
    #    return {}
    #elif req.get("result").get("action") != "Nondapp":
    #    return {}

    with open('Sheet1.json') as f:
        data = f.read()
        jsondata = json.loads(data)
    # data = json.loads(result)
    res = makeWebhookResult(jsondata)
    return res

def makejsonQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    Levp = parameters.get("BachLevp")
    Progr = parameters.get("BachSubject")
    time = parameters.get("BachTime")
    if Levp is None:
        return None
    elif Progr is None:
        return None
    elif time is None:
        return None

    match = jsonpath.jsonpath(jsondata,'$.features[[?(@.ProgramName == Progr && @.Level == Levp && @.StartDate == time)]].UniversityName,Program URL,Years,App Deadline,1stYrTuition,Tuition')
    return match


def makeWebhookResult(data):
    


    speech = "Would you like to study in " + + ": " +  + \
            ", click this link to apply to this program " ++ "With Application Deadline on " +  + \
             ",Whereby First Year Tuition fees is " +  + "In total Tuition Fees is " +  + \
             ",this program will take " +  + "Years"

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "agent"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
