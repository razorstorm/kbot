# coding=utf-8
import json
import random
import markovgen

import requests
from flask import request, Flask

app = Flask(__name__)

token = 'EAAXSUovhrQkBAJfw0cqLd1bZCpZBn9564eLqucEuJPPyZC1Gqy0AQvx6F0twfcnjtG4ZC5Ui9CFLj33cVJeS6ih86gVFYFtuzWzyGBf7SSvSO7oQHef86YMbZASBmDsPROqOktQciCs0UNfCmIFDkiseWmLM5PzHZAUhU95zx2dQZDZD'  # noqa

file_ = open('kathtest.txt')
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
    print(request.data)
    data = json.loads(request.data)

    sentences = generate_speech()

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