from flask import Flask, request
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
    print r.to_xml()
    return r.to_xml()


@app.route('/hello')
def hello():
    return 'Hello, World'

if __name__ == "__main__":
    app.run(host='0.0.0.0')
