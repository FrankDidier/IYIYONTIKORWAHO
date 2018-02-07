from __future__ import print_function
from future.standard_library import install_aliases

install_aliases()
import codecs
import csv
import json
import os
import smtplib
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


def makeWebhookResult(req):
    if req.get("result").get("action") == "DefaultFallbackIntent.DefaultFallbackIntent-custom":
        result = req.get("result")
        parameters = result.get("parameters")

        Addr = parameters.get("email")
        AddrA =''.join(Addr)

        Countr = parameters.get("geo-country")
        CountrA =''.join(Countr)
        
        ContentM = parameters.get("Seasonintake")
        ContentMA =''.join(ContentM)
        
        GiveName = parameters.get("Fname")
        GiveNameA =''.join(GiveName)
        
        LastName = parameters.get("Lname")
        LasName = ''.join(LastName)
        
        #DateEntry = parameters.get("date")
        #DateEn = ''.join(DateEntry)
        
        #LastName = parameters.get("last-name")
        
        ProgInte = parameters.get("prograinterest")
        ProgInteA =''.join(ProgInte)
        
        #PhonNumber = parameters.get("phone-number")
        #PhonNum = ''.join(PhonNumber)

        #Pr = ''.join(Progr)
        # Ti = ''.join(tme)
        #Le = ''.join(Levp)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        #server.ehlo()
        server.starttls()
        server.login("AlertTestApi2018@gmail.com", "Testapi2017")

        msg = "A user need further help at china admission -> MARCO POLO Bot -> \nGiven Name: "+str(GiveNameA)+" "+str(LasName)+"\nE-mail: "+str(AddrA)+"\nCountry: "+str(CountrA)+"\nProgram Interest: "+str(ProgInteA)+"\nStarting Date: "+str(ContentMA)
        
        #+"\nDate of data Entry: "+ DateEn 
        #+str(ContentM)
        server.sendmail("AlertTestApi2018@gmail.com", "testapiblcu2017@gmail.com", msg)
        server.quit()
    speech = "Thank you for your interest and providing the information. One of our advisors will get in contact with you soon. You can also contact us directly: wechat: china-admissions or send us an email to apply@china-admissions.com. You can also call us or add us on WhatsApp: +86 132 4122 2181"
        

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
