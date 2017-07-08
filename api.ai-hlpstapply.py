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
    
    #url = "https://raw.githubusercontent.com/FrankDidier/IYIYONTIKORWAHO/master/Sheet1.json"
    #result = urlopen(url).read()
    #jsondata = json.loads(result)

    with open('Sheet1.json') as f:
        data = f.read()
        jsondata = json.loads(data)
    
    #match = ["Hello","Bite","Nihao"]
        




    match_list = jsonpath.jsonpath(jsondata,
                              '$.features[[?(@.ProgramName == "Economics" && @.Level == "PhD" && @.StartDate == "September")]].UniversityName')
    match_str = ", ".join(match_list)


    speech = "This is the universities you were looking for " + match_str

    print("Response:")
    print(speech)

    return json.dumps({
        "displayText": speech,
        "speech": speech,
        
        # "data": data,
        # "contextOut": [[{"name":"phd", "lifespan":5}],
        "source": "marcopolo1995"
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
