import spotipy
import random

class Shuffler:
    # Spotify sp
    sp = None
    mix:dict = None # dict
    n = 0
    def __init__(self, sp) -> None:
        self.sp = sp
        
    def shuffle(self, approx_duration_ms:int=60000) -> list[str]:
        # get playlist to work with
        try:
            playlistUri = self.getNowPlayingMixUri()
        except:
            print("no mix playing")
            return []
        items = self.getMixItems(playlistUri)
        self.initialiseMix(items)
        print(self.n, self.mix)

        # select songs:
        r = self.calculateNewList(approx_duration_ms)
        uris = r['uris']
        songNames = r['names']

        playbackState = self.sp.current_playback()
        if not('pausing' in playbackState['actions']['disallows']) and playbackState['is_playing']:
            self.sp.pause_playback()
        self.sp.repeat("off")
        self.sp.shuffle("false")
        self.sp.start_playback(uris = uris)
        return songNames
    
    def calculateNewList(self, approx_duration_ms) -> dict:
        total_duration = 0
        uris = []
        songNames = []
        while total_duration < approx_duration_ms:
            randSongUri = list(self.mix.keys())[random.randrange(0, self.n)]
            uris.append(randSongUri)
            total_duration += self.mix[randSongUri]['duration_ms']
            songNames.append(self.mix[randSongUri]['name'])
        return {'uris': uris, 'names' : songNames}

    def getNowPlayingMixUri(self):
        current = self.sp.currently_playing()
        if current['context']:
            return current['context']['uri']
        raise "not playing album or playlist"

    def getMixItems(self, mixUri:str):
        playlist = self.sp.playlist(playlist_id = mixUri)
        return playlist['tracks']['items']
        

    def initialiseMix(self, items) -> None:
        mix = {}
        for item in items:
            track = item['track']
            key = track['uri']

            duration_ms = track['duration_ms']
            name = track['name']
            artist = track['artists'][0]

            mix[key] = {
                "name": name,
                'artist': artist,
                "duration_ms" : duration_ms,
            }
            self.n += 1
        self.mix = mix

        return

    @DeprecationWarning
    def getTrackUrisOfMix(self, items:list) -> list[str]: 
        uris = []
        for item in items:
            uris.append(item['track']['uri'])
        return uris
    
    @DeprecationWarning
    # very similar to above.
    def getMixDuration(self, items:list) -> int:
        duration_ms = 0
        for item in items:
            duration_ms += item['track']['duration_ms']
        return duration_ms