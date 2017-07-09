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

def getlev(reql):
    if reql.get("result").get("action") != "Phdapp":
        return {}
    result1 = reql.get("result")
    parameters = result1.get("parameters")
    Levp = parameters.get("PhDDegLevp")
    
    return Levp

def getpro(reqp):
    if reqp.get("result").get("action") != "Phdapp":
        return {}
    result2 = reqp.get("result")
    parameters = result2.get("parameters")
    Progr = parameters.get("PhDsubjects")
    
    return Progr

def gettime(reqt):
    if reqt.get("result").get("action") != "Phdapp":
        return {}
    result3 = reqt.get("result")
    parameters = result3.get("parameters")
    time = parameters.get("PhdTime")
    
    return time

def makeWebhookResult(req):
    if req.get("result").get("action") != "Phdapp":
        return {}
    #result = req.get("result")
    #parameters = result.get("parameters")

    #Progr = parameters.get("PhDsubjects")
    #time = parameters.get("PhdTime")
    #Levp = parameters.get("PhDDegLevp")
    
    
    #Levp = str(input("What level do you want to study:\n"))
    #Levp = "PhD"
    #Progr = str(input("Which subject do you want to study:\n"))
    #time = str(input("When do you want to start:\n"))

    with open('Sheet1.json') as f:
        data = f.read()
        jsondata = json.loads(data)



    match_list = jsonpath.jsonpath(jsondata,
                              '$.features[[?(@.ProgramName == getpro(reqp) && @.Level == getlev(reql) && @.StartDate == gettime(reqt))]].UniversityName,Program URL,App Deadline,1stYrTuition')
    match_str = ", #".join(match_list)


    speech = "These are the universities you were looking for with their Program direct link ,Application Deadline with first year Tuition Fees:=>" + match_str

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
