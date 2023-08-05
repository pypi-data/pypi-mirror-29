import json, os
try:
    input = raw_input # python 2
except:
    pass

class Artist(object):
    """An artist from the Genius.com database.
    
    Attributes:
        name: (str) Artist name.
        num_songs: (int) Total number of songs listed on Genius.com
    
    """                            

    def __init__(self, json_dict):
        """Populate the Artist object with the data from *json_dict*"""
        self._body = json_dict['artist']
        self._url      = self._body['url']
        self._api_path = self._body['api_path']
        self._id       = self._body['id']
        self._songs = []
        self._num_songs = len(self._songs)
        
    @property
    def name(self):            
        return str(self._body['name'].encode("utf-8", errors='ignore').decode("utf-8"))
                    
    @property
    def image_url(self):
        return self._body['image_url']
    
    @property
    def songs(self):
        return self._songs
    
    @property
    def num_songs(self):
        return self._num_songs          
        
    def add_song(self, newsong):
        """Add a Song object to the Artist object"""
        
        if any([song.title==newsong.title for song in self._songs]):
            print('{newsong.title} already in {self.name}, not adding song.'.format(newsong=newsong,self=self))
            return 1 # Failure
        if newsong.artist == self.name:
            self._songs.append(newsong)
            self._num_songs += 1
            return 0 # Success
        else:
            print("Can't add song by {newsong.artist}, artist must be {self.name}.".format(newsong=newsong,self=self))
            return 1 # Failure        
            
    def get_song(self, song_name):
        """Search Genius.com for *song_name* and add it to artist"""        
        raise NotImplementedError("I need to figure out how to allow Artist() to access search_song().")
        song = Genius.search_song(song_name,self.name)
        self.add_song(song)
        return

    def save_lyrics(self, format='json', filename=None, overwrite=False, skip_duplicates=True):
        """Allows user to save all lyrics within an Artist obejct to a .json or .txt file."""
        assert (format == 'json') or (format == 'txt'), "Format must be json or txt"

        # We want to reject songs that have already been added to artist collection
        def songsAreSame(s1, s2):
            from difflib import SequenceMatcher as sm # For comparing similarity of lyrics
            # Idea credit: https://bigishdata.com/2016/10/25/talkin-bout-trucks-beer-and-love-in-country-songs-analyzing-genius-lyrics/
            seqA = sm(None, s1.lyrics, s2['lyrics'])
            seqB = sm(None, s2['lyrics'], s1.lyrics)
            return seqA.ratio() > 0.5 or seqB.ratio() > 0.5

        def songInArtist(new_song):    
            # artist_lyrics is global (works in Jupyter notebook)
            for song in lyrics_to_write['songs']:
                if songsAreSame(new_song, song):
                    return True
            return False

        # Determine the filename
        if filename is None:
            filename = "Lyrics_{}.{}".format(self.name.replace(" ",""), format)
        else:
            filename = filename.split('.')[0] + '.' + format
            
        # Check if file already exists    
        write_file = False
        if not os.path.isfile(filename):
            write_file = True
        elif overwrite:
            write_file = True
        else:
            if input("{} already exists. Overwrite?\n(y/n): ".format(filename)).lower() == 'y':
                write_file = True
                
        # Format lyrics in either .txt or .json format
        if format == 'json':
            lyrics_to_write = {'songs': [], 'name': self.name}
            for song in self.songs:
                if skip_duplicates is False or not songInArtist(song): # This takes way too long! It's basically O(n^2), can I do better?
                    lyrics_to_write['songs'].append({})
                    lyrics_to_write['songs'][-1]['title']  = song.title
                    lyrics_to_write['songs'][-1]['album']  = song.album
                    lyrics_to_write['songs'][-1]['year']   = song.year
                    lyrics_to_write['songs'][-1]['lyrics'] = song.lyrics                
                    lyrics_to_write['songs'][-1]['image']  = song.song_art_image_url
                    lyrics_to_write['songs'][-1]['artist'] = self.name
                    lyrics_to_write['songs'][-1]['json']   = song._body
                else:
                    print("SKIPPING \"{}\" -- already found in artist collection.".format(song.title))
        else:
            lyrics_to_write = " ".join([s.lyrics + 5*'\n' for s in self.songs])

        # Write the lyrics to either a .json or .txt file
        if write_file:
            with open(filename, 'w') as lyrics_file:
                if format == 'json':                    
                    json.dump(lyrics_to_write, lyrics_file)
                else:    
                    lyrics_file.write(lyrics_to_write)
            print('Wrote {} songs to {}.'.format(self.num_songs, filename))
        else:
            print('Skipping file save.\n')    
        return lyrics_to_write

    def __str__(self):
        """Return a string representation of the Artist object."""                        
        if self._num_songs == 1:
            return '{0}, {1} song'.format(self.name,self._num_songs)
        else:
            return '{0}, {1} songs'.format(self.name,self._num_songs)
    
    def __repr__(self):
        return repr((self.name, '{0} songs'.format(self._num_songs))) 