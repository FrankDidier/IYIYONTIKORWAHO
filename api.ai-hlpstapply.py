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

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def makeWebhookResult(req):
    if req.get("result").get("action") != "Phdapp":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")

    Progr = parameters.get("PhDsubjects")
    time = parameters.get("PhdTime")
    Levp = parameters.get("PhDDegLevp")

    with open('Sheet1.json') as f:
        data = f.read()
        jsondata = json.loads(data)




    match = jsonpath.jsonpath(jsondata,
                              '$.features[[?(@.ProgramName == Progr && @.Level == Levp && @.StartDate == time)]].UniversityName,Program URL,Years,App Deadline,1stYrTuition,Tuition')
    # return match

    # speech = "Would you like to study in " + Univname + ": " + progname + \
    #         ", click this link to apply to this program " + progurl + "With Application Deadline on " + Appdead + \
    #         ",Whereby First Year Tuition fees is " + FirstTuit + "In total Tuition Fees is " + Tuit + \
    #         ",this program will take " + yaz + "Years"


    speech = "Hello this is your webhook call i am here for you"

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [[{"name":"phd", "lifespan":5}],
        "source": "marcopolo1995"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
