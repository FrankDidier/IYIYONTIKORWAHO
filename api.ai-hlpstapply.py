from __future__ import print_function
from future.standard_library import install_aliases

install_aliases()
import codecs
import csv
import json
import os
# import jsonpath
# from jsonpath_rw import jsonpath, parse
# import jsonpath_rw

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

def makeWebhookResult(req):
    if req.get("result").get("action") == "Phdapp":
        result = req.get("result")
        parameters = result.get("parameters")

        Progr = parameters.get("PhDsubjects")

        tme = parameters.get("PhdTime")

        Levp = parameters.get("PhDDegLevp")

        Pr = ''.join(Progr)
        Ti = ''.join(tme)
        Le = ''.join(Levp)

    #query = 'Program_Name == Pr and Level == Le and Start_Date == Ti'
    query = 'id > 36 and code_name == "def" and value <=100'
    csvData = csv.reader(codecs.open('myData.csv', 'rb', encoding='latin-1'))
    csvTable = []
    isHeader = True
    for row in csvData:
        if isHeader:
            isHeader = False
            headerRow = row
            for i in range(len(headerRow)):
                headerRow[i] = headerRow[i].replace(' ', '_')
        else:
            csvTable.append(row)
    colType = []
    for i in range(len(headerRow)):
        isFloat = True
        isInt = True
        for j in range(len(csvTable)):
            try:
                v = float(csvTable[j][i])
                if not v == int(v):
                    isInt = False
            except ValueError:
                isFloat = False
                isInt = False

        colT = ''
        if isInt:
            colT = 'int'
        elif isFloat:
            colT = 'float'
        else:
            colT = 'string'
        colType.append(colT)

    for j in range(len(csvTable)):
        for i in range(len(headerRow)):
            if colType[i] == 'string':
                exec(headerRow[i] + '=' + '"' + csvTable[j][i] + '"')
            elif colType[i] == 'float':
                exec(headerRow[i] + '=' + 'float("' + csvTable[j][i] + '")')
            elif colType[i] == 'int':
                exec(headerRow[i] + '=' + 'int("' + csvTable[j][i] + '")')
        if eval(query):
            t=csvTable[j]
            o=csvTable[j+1]
            #u='    =>'.join(t)
        #print(headerRow)
        t=csvTable[j]
        j += -1
        o=csvTable[j]

    #t = csvTable[j]
    #match_str = ", #".join(u)
    speech = "These are universities you were looking for :) with their Program direct-link ,Application Deadline with first year Tuition Fees:=>" + t + "," + o
        # str(match_list) + t
        # + json.dumps(Progr) + yes

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
