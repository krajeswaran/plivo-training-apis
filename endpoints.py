from flask import Flask, request, Response, url_for
import plivoxml, plivo

app = Flask(__name__)

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
    getDigits = plivoxml.GetDigits(action=getdigits_action_url,
            method='GET', timeout=7, numDigits=1,
            retries=1, redirect='false')
    getDigits.addSpeak("Press 1 to transfer this call")
    r.add(getDigits)
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
    auth_id = "MAMZAYOTJJMDM3NDQ2OT"
    auth_token = "ODE1ZmJkNzI3MzIwMmNmMDBiMDFiNjkxMDhlMjZj"
    print ("Call UUID is : %s") % (call_uuid)
    print ("Digit pressed is : %s")  % (digit)
    p = plivo.RestAPI(auth_id, auth_token)
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
    getDigits = plivoxml.GetDigits(action=getdigits_action_url,
            method='POST', timeout=7, numDigits=1,
            retries=1, redirect='false')

    getDigits.addSpeak("Welcome to Plivo Training IVR")
    r.add(getDigits)
    r.addSpeak("You haven't pressed any valid keys")
    print (r.to_xml())
    return Response(str(r), mimetype='text/xml')



@app.route('/ivr/next', methods=['POST', 'GET'])
def ivr_next():
    response = plivoxml.Response()
    digit = request.form.get('Digits')
    if digit == "1":
        # Read out a text.
        response.addSpeak("You pressed one")
    elif digit == "2":
        # Listen to a song
        response.addPlay("https://upload.wikimedia.org/wikipedia/commons/6/6a/04_%D0%B8%D0%BA%D0%BE%D1%81_1.oggvorbis.ogg")
    else:
        response.addSpeak("I'm not angry with you, just disappointed!")

    return Response(str(response), mimetype='text/xml')



@app.route('/')
def index():
    return 'Hello, World'

if __name__ == "__main__":
    app.run(host='0.0.0.0')
