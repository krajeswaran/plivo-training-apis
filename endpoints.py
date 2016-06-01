from flask import Flask, request, Response, url_for
import os
import plivoxml, plivo

app = Flask(__name__)

PLIVO_AUTH_ID = os.environ.get('PLIVO_AUTH_ID')
PLIVO_AUTH_TOKEN = os.environ.get('PLIVO_AUTH_TOKEN')

@app.route('/message', methods=['POST', 'GET'])
def message():
    # Sender's phone number
    from_number = request.values.get('From')
    # Receiver's phone number - Plivo number
    to_number = request.values.get('To')
    # The text which was received
    text = request.values.get('Text')

    params = {
     "src": to_number,
     "dst": from_number,
    }
    body = "Thanks, we've received your message."

    r = plivoxml.Response()
    r.addMessage(body, **params)
    print (r.to_xml())
    return Response(str(r), mimetype='text/xml')


@app.route('/speak', methods=['POST', 'GET'])
def speak():
    r = plivoxml.Response()
    r.addSpeak("Thanks for calling!")
    print (r.to_xml())
    return Response(str(r), mimetype='text/xml')


@app.route('/forward', methods=['POST', 'GET'])
def forward():
    r = plivoxml.Response()
    r.addSpeak("Thanks for calling Plivo training!. Your call is now being forwarded")
    forwardNumber = "919952899700"
    r.addDial().addNumber(forwardNumber)
    print (r.to_xml())
    return Response(str(r), mimetype='text/xml')


@app.route('/conference', methods=['POST', 'GET'])
def conference():
    r = plivoxml.Response()
    r.addSpeak("Thanks for calling Plivo training conference!")
    conferenceName= "Plivo Test Conference"
    r.addConference(conferenceName)
    print (r.to_xml())
    return Response(str(r), mimetype='text/xml')


@app.route('/transfer', methods=['POST', 'GET'])
def transfer():
    r = plivoxml.Response()
    getdigits_action_url = url_for('transfer_action', _external=True)
    get_digits = plivoxml.GetDigits(action=getdigits_action_url,
            method='GET', timeout=7, numDigits=1,
            retries=1, redirect='false')
    get_digits.addSpeak("Press 1 to transfer this call")
    r.add(get_digits)
    params = {
        'length' : "10" # Time to wait in seconds
    }
    r.addWait(**params)
    print (r.to_xml())
    return Response(str(r), mimetype='text/xml')


@app.route('/transfer_action/', methods=['POST', 'GET'])
def transfer_action():
    digit = request.args.get('Digits')
    call_uuid = request.args.get('CallUUID')
    print ("Call UUID is : %s") % (call_uuid)
    print ("Digit pressed is : %s")  % (digit)
    p = plivo.RestAPI(PLIVO_AUTH_ID, PLIVO_AUTH_TOKEN)
    if digit == "1":
        params = {
            'call_uuid' : call_uuid, # ID of the call
            'aleg_url' : "http://plivo-flask-training.herokuapp.com/forward", # URL to transfer for aleg
            'aleg_method' : "GET" # ethod to invoke the aleg_url
        }
        response = p.transfer_call(params)
    else :
        print ("Wrong Input")
        print (str(response))

    return Response(str(response), mimetype='text/plain')


@app.route('/ivr/start', methods=['POST', 'GET'])
def ivr_start():
    r = plivoxml.Response()
    getdigits_action_url = url_for('ivr_next', _external=True)
    get_digits = plivoxml.GetDigits(action=getdigits_action_url,
            method='GET', timeout=7, numDigits=1,
            retries=2, redirect='true')

    get_digits.addSpeak("Welcome to Plivo Training IVR")
    r.add(get_digits)
    r.addSpeak("You haven't pressed any valid keys")
    print (r.to_xml())
    return Response(str(r), mimetype='text/xml')


@app.route('/ivr/next', methods=['POST', 'GET'])
def ivr_next():
    response = plivoxml.Response()
    digit = request.values.get('Digits')
    print (digit)
    if digit == "1":
        # Read out a text.
        response.addSpeak("You pressed one")
    elif digit == "2":
        # Patch to one number
        response.addSpeak("You are now being patched..")
        forwardNumber = "919952899700"
        params = { 'dialMusic': 'real' }
        response.addDial(**params).addNumber(forwardNumber)
    elif digit == "3":
        # call record
        response.addSpeak("Talk to the hand.")
        record_params = { 'action': 'http://requestb.in/15j1zi21', 'maxLength' : '50', 'finishOnKey': '*' }
        response.addRecord(**params)
        response.addSpeak("You dummy.")
    else:
        response.addSpeak("I'm not angry with you, I'm just disappointed!")

    return Response(str(response), mimetype='text/xml')



@app.route('/')
def index():
    return 'Hello, World'

if __name__ == "__main__":
    app.run(host='0.0.0.0')
