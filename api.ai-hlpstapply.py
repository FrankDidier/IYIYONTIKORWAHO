#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases

install_aliases()

import json
import os
import jsonpath
#from jsonpath_rw import jsonpath, parse
#import jsonpath_rw

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
#
def trial(req):
    if req.get("result").get("action") == "Phdapp":
        result = req.get("result")
        parameters = result.get("parameters")

        Progr = parameters.get("PhDsubjects")
        Pr=''.join(Progr)
        
        return Pr
def makeWebhookResult(req):
    if req.get("result").get("action") == "Phdapp":
        result = req.get("result")
        parameters = result.get("parameters")

        #Progr = parameters.get("PhDsubjects")
    
        tme = parameters.get("PhdTime")
    
        Levp = parameters.get("PhDDegLevp")
        
        #Pr=''.join(Progr)
        #A = json.loads(Pr)
        #yes=json.dumps(Pr)
        #A=str(Pr)
        #Ti=''.join(tme)
        #qew=json.dumps(Ti)
        #B=str(Ti)
        #Le=''.join(Levp)
        #vbe=json.dumps(Le)
        #C=str(Le)
        
    

    with open('Sheet1.json') as f:
        data = f.read()
        jsondata = json.loads(data)
    #using Jsonpath_rw
    #match_list = jsonpath_rw.parse("$.features[[?(@.ProgramName == A && @.Level == C  && @.StartDate == B )]].UniversityName,Program URL,App Deadline,1stYrTuition").find(jsondata)
    #y="bachelor's"
    #Using jsonpath
    t="{}".format(trial(req))
    match_list = jsonpath.jsonpath(jsondata,
                              '$.features[[?(@.ProgramName == t && @.Level == "PhD"  && @.StartDate == "September" )]].UniversityName,Program URL,App Deadline,1stYrTuition')
    
    
    #match_str = ", #".join(match_list)
#

    speech = "These are universities you were looking for :) with their Program direct-link ,Application Deadline with first year Tuition Fees:=>" + str(match_list) + t
    #+ json.dumps(Progr) + yes

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        
        #"data": [],
        # "contextOut": [[{"name":"phd", "lifespan":5}],
        "source": "marcopolo1995"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
