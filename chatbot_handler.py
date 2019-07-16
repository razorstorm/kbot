# coding=utf-8
import json
import random
import markovgen

import requests
from flask import request, Flask

app = Flask(__name__)

token = 'EAAgZAanyls4sBAN12HSpOt7txZABocVsuw1GchwcUNUIRXayXpmXudAa1poT0bnsjI5LZBByvItdJv2yGLA6KStAwMguTAvlm5ZBGK56dSv9oLkCZCRcxKtQ0j21pg4SAUShyeK9wbqdWrtutoybmLuG3iw469ZCucrGG3kI9ko1ZAlBZC9q8C59'  # noqa

file_ = open('messages.txt')
markov = markovgen.Markov(file_)



@app.route('/receive', methods=['GET'])
def serve():
    if (
        request.args.get('hub.mode') == 'subscribe' and
        request.args.get('hub.verify_token') == 'the'
    ):
        return request.args.get('hub.challenge')
    return 'the'


def generate_speech():
    return markov.generate_markov_text()


@app.route('/receive', methods=['POST'])
def receive():
    sentences = generate_speech()

    print(request.data)
    print(request.__dict__)
    data = json.loads(request.data)

    try:
        for entry in data['entry']:
            for message in entry['messaging']:
                sender = message['sender']['id']

                resp_msg = {
                    'recipient': {
                        'id': sender,
                    },
                    'message': {
                        'text': sentences,
                    },
                }

                response = requests.post(
                    'https://graph.facebook.com/v2.6/me/messages',
                    params={'access_token': token},
                    json=resp_msg,
                )
                print('Sent requests %s' % json.dumps(resp_msg))
                print('Received response %s' % response.text)
    except Exception as e:
        print(e)
        return 'not handled'

    return 'success'