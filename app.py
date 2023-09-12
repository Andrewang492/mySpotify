import time
from flask import Flask, request, url_for, session, redirect
import spotipy #spotipy is an app that wraps spotify API in a module.
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import helper
import json
import shufflePlus

SCOPE = "user-read-playback-state user-modify-playback-state user-read-currently-playing"

app = Flask(__name__)

app.secret_key = "asdfasds" # a random string used to sign the session cookie
app.config['SESSION_COOKIE_NAME'] = 'my cookie' #a session is where we store data of a user's session, ie dont need login to different pages because in a session.

@app.route('/')
def home():
    return "home"


@app.route('/login')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth() #create a new one...
    session.clear() # in this redirected state, clear everything else????
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(as_dict = True, code = code) #tokeninfo has refresh token, access token, expiresAt.
    session["token_info"] = token_info #save this token information in this session.
    return redirect(url_for('shuffle')) #then send back to front end.

@app.route('/shuffle')
def shuffle():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect(url_for('login', _external = False))
    sp = spotipy.Spotify(auth = token_info['access_token'])
    shuffler = shufflePlus.Shuffler(sp)
    uris = shuffler.shuffle(approx_duration_ms=1000*60*60*3)
    return {'value': uris} 

@app.route('/getSomething')
def getSomething():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect(url_for('login', _external = False))
    h = helper.Instance(spotipy.Spotify(auth = token_info['access_token']))

    #return {'value': h.getTrackUrisOfList("spotify:playlist:7nHGruGncwKc1yyKTqPQcA")}
    return h.getNowPlaying()

def get_token():
    token_info = session.get("token_info", None) # i.e if token info doesnt exist this is None.
    if not token_info:
        print("can't find token")
        raise "exception"
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info

# Authorisation - get your user to tell Spotify that you are allowed information.
# Spotify will give you an access code that you use to get Tokens. that you can make requests with.
clientID = "7ffd96410f9c47b7a37ba0908fb71d2b"
clientSecret = "09843f4c77f14d66b391ea06dcc67a99"


def create_spotify_oauth():
    #make this special object. Every time you use need this object, make a new one.
    return SpotifyOAuth(
        client_id = clientID,
        client_secret = clientSecret,
        #redirect_uri = url_for('redirectPage', _external = True),
        redirect_uri = 'http://127.0.0.1:8080/redirect',
        scope = SCOPE
    )

if __name__ == '__main__':
    app.run(debug=True, port=8080)
