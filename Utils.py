from dotenv import load_dotenv
import requests
import os


CALLBACK_URL = ""
OUTPUT = None #Username of of streamer which you want to see the chat of.

def get_token():
    load_dotenv()
    return os.getenv('TOKEN')

def get_client_id():
    load_dotenv()
    return os.getenv('CLIENT_ID')

def get_app_client_secret():
    load_dotenv()
    return os.getenv('APP_CLIENT_SECRET')

def get_app_client_id():
    load_dotenv()
    return os.getenv('APP_CLIENT_ID')

def get_callback_url():
    return CALLBACK_URL

def set_callback_url(url):
    global CALLBACK_URL
    CALLBACK_URL = url
    
def streamer_to_id(username: str) -> int:
    token = get_token()
    client_id = get_client_id()
    # Function to get the user ID from the username
    headers = {
        'Client-ID': f'{client_id}',
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(
        f'https://api.twitch.tv/helix/users?login={username}',
        headers=headers
    )
    # print(response.json())
    return response.json()['data'][0]['id']

def create_clip(broadcaster_id):
    # Function to create a clip
    headers = {
        'Client-ID': get_client_id(),
        'Authorization': f'Bearer {get_token()}'
    }
    response = requests.post(
        f'https://api.twitch.tv/helix/clips?broadcaster_id={broadcaster_id}',
        headers=headers
    )

    print(response.json())
    if response.status_code == 202:
        return response.json()['data'][0]['id'], response.json()['data'][0]['edit_url']
    else:
        print("ERROR: Clip creation failed.")
        return None, None
    

def get_access_token():
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': get_app_client_id(),
        'client_secret': get_app_client_secret(),
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, params=params)
    return response.json()['access_token']

def read_current_user_id():

    IDS = []
    
    with open('current_user_ids') as file:
        for line in file:
            IDS.append(line.strip())
    return IDS

def save_user_ids(user_ids):
    with open('current_user_ids', 'a') as file:
        for user_id in user_ids:
            file.write(user_id + '\n')
    return


def check_stream_status(username: str) -> bool:
    token = get_token()
    client_id = get_client_id()
    headers = {
        'Client-ID': f'{client_id}',
        'Authorization': f'Bearer {token}'
    }
    params = {
        'user_login': username
    }

    response = requests.get(
        'https://api.twitch.tv/helix/streams',
        headers=headers,
        params=params
    )
    data = response.json()
    if not data:
        raise Exception('No data returned from Twitch API')
    if data['data']:
        return True
    else:
        return False