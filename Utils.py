from dotenv import load_dotenv
import requests
import os

def get_token():
    load_dotenv()
    return os.getenv('TOKEN')

def get_client_id():
    load_dotenv()
    return os.getenv('CLIENT_ID')

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

