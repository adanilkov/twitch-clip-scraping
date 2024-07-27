from flask import Flask, request, jsonify
import requests
import json
import Utils as utils

app = Flask(__name__)

USER_IDS = []

def subscribe_to_stream_online(NEW_USER_ID, CALLBACK_URL):
    url = 'https://api.twitch.tv/helix/eventsub/subscriptions'
    headers = {
        'Client-ID': utils.get_app_client_id(),
        'Authorization': f'Bearer {utils.get_access_token()}',
        'Content-Type': 'application/json'
    }
    data = {
        'type': 'stream.online',
        'version': '1',
        'condition': {
            'broadcaster_user_id': NEW_USER_ID
        },
        'transport': {
            'method': 'webhook',
            'callback': CALLBACK_URL,
            'secret': utils.get_app_client_secret() 
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.json())

def unsubscribe_all():
    url = 'https://api.twitch.tv/helix/eventsub/subscriptions'
    headers = {
        'Client-ID': utils.get_app_client_id(),
        'Authorization ': f'Bearer {utils.get_access_token()}'
    }
    response = requests.get(url, headers=headers)
    print(response.json())
    for sub in response.json()['data']:
        response = requests.delete(url + f'/{sub["id"]}', headers=headers)
        print(response.json())
        

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if request.headers.get('Twitch-Eventsub-Message-Type') == 'webhook_callback_verification':
        return data['challenge']
    if request.headers.get('Twitch-Eventsub-Message-Type') == 'notification':
        # TODO here
        # Handle the stream online notification
        print('Stream Online:', data)
        return jsonify({'status': 'success'})
    return jsonify({'status': 'ignored'})


app.run(host='0.0.0.0', port=5000)
