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



    match_list = jsonpath.jsonpath(jsondata,
                              '$.features[[?(@.ProgramName == Progr && @.Level == Levp && @.StartDate == time)]].UniversityName,Program URL,App Deadline,1stYrTuition')
    match_str = ", ".join(match_list)


    speech = "These are the universities you were looking for with the program name/direct link also with Application Deadline with their first year Tuition Fees:=>" + match_str

    print("Response:")
    print(speech)

    return json.dumps({
        "speech": speech,
        "displayText": speech,
        
        # "data": data,
        # "contextOut": [[{"name":"phd", "lifespan":5}],
        "source": "marcopolo1995"
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
