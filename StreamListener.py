from flask import Flask, request, jsonify
import requests
import json
import Utils as utils

app = Flask(__name__)


USER_IDS = []
# # Your Twitch client ID and secret
# CLIENT_ID = 'your_client_id'
# CLIENT_SECRET = 'your_client_secret'
# USER_ID = 'target_user_id'  # The user ID of the streamer you want to monitor
# CALLBACK_URL = 'your_callback_url'  # Your public URL where Twitch will send notifications



def get_access_token():
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': utils.get_app_client_id(),
        'client_secret': utils.get_app_client_secret(),
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, params=params)
    return response.json()['access_token']

def subscribe_to_stream_online(NEW_USER_ID, CALLBACK_URL):
    url = 'https://api.twitch.tv/helix/eventsub/subscriptions'
    headers = {
        'Client-ID': utils.get_app_client_id(),
        'Authorization': f'Bearer {get_access_token()}',
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
            'secret': 'your_secret'  # Secret for verifying message signatures
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.json())

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if request.headers.get('Twitch-Eventsub-Message-Type') == 'webhook_callback_verification':
        return data['challenge']
    if request.headers.get('Twitch-Eventsub-Message-Type') == 'notification':
        # Handle the stream online notification
        print('Stream Online:', data)
        return jsonify({'status': 'success'})
    return jsonify({'status': 'ignored'})

if __name__ == '__main__':
    # Subscribe to the stream.online event when the app starts
    subscribe_to_stream_online()
    app.run(host='0.0.0.0', port=5000)
