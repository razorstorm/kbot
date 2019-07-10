import json

with open('messages.json', 'r') as fh:
    with open('messages.txt', 'w') as output:
        b = json.loads(fh.read())
        messages = b['messages']
        for message in messages:
            if 'sender_name' in message and 'content' in message:
                if message['sender_name'] == 'Karen Sin':
                    print(message['sender_name'], message['content'])
                    output.write(message['content'] + "\n")
