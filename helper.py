import spotipy
import random

class Instance:
    # Spotify sp
    sp = None
    def __init__(self, sp) -> None:
        self.sp = sp

    def getATrack(self):
        items = self.sp.current_user_saved_tracks(limit=50, offset=0)['items']
        track1 = items[random.randrange(0,50)]['track']
        
        artists = ""
        for artist in track1['artists']:
            artists = f"{artists} {artist['name']},"
        name1 = track1['name']
        return f"{artists} | {name1}"


    def getCurrentUser(self):
        return self.sp.me()

    def getPlaybackState(self):
        return self.sp.current_playback()

    def getSomeSong(self, query):
        return self.sp.search(query, limit=2, type='track')

    def getUserPlaylists(self):
        return self.sp.current_user_playlists()

    def getUserPlaylistNames(self):
        ans = ""    
        for item in self.sp.current_user_playlists()['items']:
            ans = f"|||||||{ans} {item['name']} {item['id']}||||||"
        return ans
    def getPlaylist(self, id):
        return self.sp.playlist(playlist_id = id)

    def getNowPlaying(self):
        return self.sp.currently_playing()
    
    def getNowPlayingList(self):
        current = self.sp.currently_playing()
        if current['context']:
            return current['context']['uri']
        else:
            return "not playing album or playlist"
    
    def getTrackUrisOfList(self, playlistUri:str) -> list[str]:
        playlist = self.sp.playlist(playlist_id = playlistUri)
        items = playlist['tracks']['items']
        uris = []
        for item in items:
            uris.append(item['track']['uri'])
        return uris

    def togglePlayback(self):
        sp = self.sp

        playbackState = sp.current_playback()
        if 'pausing' in playbackState['actions']['disallows'] or not playbackState['is_playing']:
            sp.start_playback(uris = ["spotify:track:3xMnPIvsaWwzHzqqzaihEX",
                                    "spotify:track:5Lv5L45PQmp5CTjs5PlQ6e",
                                    "spotify:track:5Lv5L45PQmp5CTjs5PlQ6e",
                                    "spotify:track:3xMnPIvsaWwzHzqqzaihEX"])
            #spotify:track:5Lv5L45PQmp5CTjs5PlQ6e silk cologne
        elif 'resuming' in playbackState['actions']['disallows'] or playbackState['is_playing']:
            sp.pause_playback()
        return
