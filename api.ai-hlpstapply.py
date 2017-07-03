#!/usr/bin/env python

import urllib
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

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "Bachapp":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    Levp = parameters.get("BachLevp")
    Progr = parameters.get("BachSubject")
    time = parameters.get("BachTime")
    
    with open('Sheet1.json') as f:
        data = f.read()
        jsondata = json.loads(data)
        
    match = jsonpath.jsonpath(jsondata,'$.features[[?(@.ProgramName == Progr && @.Level == Levp && @.StartDate == time)]].UniversityName,Program URL,Years,App Deadline,1stYrTuition,Tuition')    
    


    speech = "The info about bachelor's degree are " + match + "Thank you"

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "agent"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
