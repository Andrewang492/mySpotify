import spotipy
import random
from waitTimeManager import waitTimeManager

class Shuffler:
    # Spotify sp
    sp = None
    mix:dict = None
            #  mix[key] = {
            #     "name": name,
            #     'artist': artist,
            #     "duration_ms" : duration_ms,
            # }
    n = 0
    def __init__(self, sp) -> None:
        self.sp = sp
        
    def shuffle(self, approx_duration_ms:int=60000) -> list[str]:
        # get playlist to work with
        try:
            playlistUri = self.__getNowPlayingMixUri()
        except:
            print("no mix playing")
            return []
        self.__initialiseMix(playlistUri)

        # select songs:
        r = self.__calculateNewList(approx_duration_ms)
        uris = r['uris']        
        self.__beginPlaying(uris)
        songNames = r['names']
        return songNames

    def __initialiseMix(self, mixUri) -> None:
        playlist = self.sp.playlist(playlist_id = mixUri)
        items = playlist['tracks']['items']
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

    def __beginPlaying(self, uris:list):
        playbackState = self.sp.current_playback()
        if not('pausing' in playbackState['actions']['disallows']) and playbackState['is_playing']:
            self.sp.pause_playback()
        self.sp.repeat("off")
        self.sp.shuffle(False)
        self.sp.start_playback(uris = uris)

    # Select shuffle type by changing name of shuffle function:
    def __calculateNewList(self, approx_duration_ms) -> dict:
        return self.__waitingShuffle(approx_duration_ms)

    # Each track always has equal chance of playing
    def __uniformShuffle(self, approx_duration_ms, maxSongs = 100) -> dict:
        total_duration = 0
        queue = []
        songNames = []
        i = 0
        while total_duration < approx_duration_ms and i < maxSongs:
            randSongUri = list(self.mix.keys())[random.randrange(0, self.n)]
            queue.append(randSongUri)
            total_duration += self.mix[randSongUri]['duration_ms']
            songNames.append(self.mix[randSongUri]['name'])
            i += 1
        return {'uris': queue, 'names' : songNames}

    # Inserts single copies until they've all played. Repeat.
    def __cyclicShuffle(self, approx_duration_ms, maxSongs = 100) -> dict:
        total_duration = 0
        i = 0
        uris = list(self.mix.keys())
        queue = []
        songNames = []
        
        while total_duration < approx_duration_ms and i < maxSongs:
            if len(uris) == 0:
                uris = list(self.mix.keys())
            randSongUri = uris.pop(random.randrange(0, len(uris)))

            queue.append(randSongUri)
            songNames.append(self.mix[randSongUri]['name'])
            i += 1
            total_duration += self.mix[randSongUri]['duration_ms']

        return {'uris': queue, 'names' : songNames}

    # 
    def __waitingShuffle(self, approx_duration_ms, maxSongs = 100) -> dict:
        total_duration = 0
        queue = [] #of uris
        songNames = []
        i = 0
        #initialise PDF:
        waitManager = waitTimeManager(self.mix)

        while total_duration < approx_duration_ms and i < maxSongs:
            # create cumulative distribbution: [(,), (,)...]
            # random number used to binary search for key. (ascending)
            randSongUri = waitManager.getRandomSong()

            trackDuration = self.mix[randSongUri]['duration_ms']
            waitManager.increaseWaitTimes(trackDuration, randSongUri)
            queue.append(randSongUri)
            total_duration += trackDuration
            songNames.append(self.mix[randSongUri]['name'])
            i += 1
        return {'uris': queue, 'names' : songNames}

    
    
    def __getNowPlayingMixUri(self):
        current = self.sp.currently_playing()
        if current['context']:
            return current['context']['uri']
        raise "not playing album or playlist"
        
        


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