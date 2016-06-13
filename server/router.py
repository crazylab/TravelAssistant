from flask import Flask, request, Response

app = Flask(__name__.split('.')[0])

PORT = 8080


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return 'Server is running on port %s' % str(PORT)


# Setup of validation tokens are needed here
VALIDATION_TOKEN = 'This_is_the_validation_token'
PAGE_TOKEN = 'set_the_page_token_here'


@app.route('/webhook', methods=['GET'])
def validate_webhook():
    if request.args['hub.mode'] == 'subscribe' and request.args['hub.verify_token'] == VALIDATION_TOKEN:
        print 'Validating webhook'
        hub_challenge = request.args['hub.challenge']
        return Response(response=hub_challenge, status=200)
    else:
        print 'Failed validation. Make sure the validation tokens match.'
        return Response(status=403)


def errorHandler(error, response, body):
    if error:
        print 'Error sending message: ' + error
    elif response.body.error:
        print 'Error: ' + response.body.error


def sendTextMessage(sender, message):
    messageHead = {
        'url': 'https://graph.facebook.com/v2.6/me/messages',
        'qs': {'access_token': PAGE_TOKEN},
        'method': 'POST',
        'json': {
            'recipient': {'id': sender},
            'message': {'text': message}
        }
    }
    request(messageHead, errorHandler)


@app.route('/webhook', methods=['POST'])
def receive_message():
    data = request.values
    messaging_event = data.entry[0].messaging

    for index in range(len(messaging_event)):
        event = data.entry[0].messaging[index]
        sender = event.sender.id

        if event.message and event.message.text:
            text = event.message.text
            print "Message " + text
            sendTextMessage(sender, "I'm Bot")

    return Response(status=200)


app.run(debug=True, port=PORT)
