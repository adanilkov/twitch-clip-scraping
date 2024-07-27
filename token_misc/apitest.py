import requests

class test:
    def __init__(self):
        self.token = 'exgk16wl7qep8qz1kregg7cz60z7k9'
        self.client_id = 'gbeyk8mydvhi9q4mdebwmq2buotv7w'


    def create_clip(self, broadcaster_id):
        # Function to create a clip
        headers = {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {self.token}'
        }
        response = requests.post(
            f'https://api.twitch.tv/helix/clips?broadcaster_id={broadcaster_id}',
            headers=headers
        )

        print(response.status_code)
        print(response.json())

test().create_clip(598903130) 