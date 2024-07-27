from flask import Flask, redirect, request, url_for
import urllib.parse

app = Flask(__name__)

CLIENT_ID = 'gbeyk8mydvhi9q4mdebwmq2buotv7w'
REDIRECT_URI = 'http://localhost:3000'
SCOPE = 'clips:edit'


@app.route('/start')
def home():
    # Construct the authorization URL
    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'token',  # Make sure to use 'token' for implicit grant flow
        'scope': SCOPE,
    }
    auth_url = f"https://id.twitch.tv/oauth2/authorize?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)

@app.route('/')
def callback():
    # Access the URL fragment from the full URL
    fragment = request.url.split('#')[1] if '#' in request.url else ''
    if fragment:
        # Extract the access token from the URL fragment
        token_info = dict(item.split("=") for item in fragment.split("&"))
        access_token = token_info.get('access_token')

        if access_token:
            return f"Access Token: {access_token}"
        else:
            return "Error: Access token not found."
    else:
        return "Error: No URL fragment found. Make sure the response type is 'token'."

if __name__ == "__main__":
    app.run(debug=True, port=3000)
