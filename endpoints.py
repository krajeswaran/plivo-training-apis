from flask import Flask, request, Response
import plivoxml, plivo

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
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
    r.addSpeak("Thanks for calling Plivo training!")
    forwardNumber = "919952899700"
    d = r.addDial()
    d.addNumber(forwardNumber)
    # r.addDial().addNumber(forwardNumber)
    print (r.to_xml())
    return Response(str(r), mimetype='text/xml')


@app.route('/hello')
def hello():
    return 'Hello, World'

if __name__ == "__main__":
    app.run(host='0.0.0.0')
