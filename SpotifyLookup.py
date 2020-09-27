import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials

import string
import Levenshtein as lev
import re

SPOTIPY_CLIENT_ID = 'a5ad437675474f19bc6c76bb096dee85'
SPOTIPY_CLIENT_SECRET = '69b402da629b41d498354ae80444c3d9'

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET))

########## Spotify lookup ############

def spotify_lookup (artist_name):

    # Reset spotify values
    spotify_match = False
    artist_name_spotify = ""
    artist_img_spotify = ""
    artist_spotify_id = ""
    subgenres_spotify = []
    artist_popularity_spotify = ""

    try:
        # Preprocessing: Remove all within () and punctuation, set lowercase
        preprocessed_name = re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", artist_name)
        preprocessed_name = preprocessed_name.lower()
        preprocessed_name = preprocessed_name.translate(str.maketrans('', '', string.punctuation))
        print('Name preprocessing:', artist_name, '=', preprocessed_name)

        # Make Spotify lookup on raw artist name
        results = spotify.search(q='artist:' + artist_name, type='artist')
        items = results['artists']['items']

        # If spotify returns no results on raw artist name search, make Spotify lookup on preprocessed artist name

        if len(items) == 0:
            print('No result on raw name, trying preprocessed name...')
            results = spotify.search(q='artist:' + preprocessed_name, type='artist')
            items = results['artists']['items']

        # If spotify returns results on raw artist name
        if len(items) > 0:

            print('found', len(items), 'results')
            print('searching for exact string match...')

            # First check all results for exact string match
            for ii in range(len(items)):
                artist = items[ii]

                # Set lower case and match songkick name with spotify name
                if artist_name.lower() == artist['name'].lower():

                    spotify_match = True
                    print('Found exact string match on index', ii, artist['name'])

                    artist_name_spotify = artist['name']
                    artist_img_spotify = artist['images'][0]['url']
                    artist_spotify_id = artist['id']
                    subgenres_spotify = artist['genres']
                    artist_popularity_spotify = artist['popularity']

                    break

                else:
                    print('No exact match on result from index ', ii, artist['name'])

            # If no match, then check all spotify results for fuzzy string match above 90%
            if spotify_match == False:
                print('searching for fuzzy string match...')

                for iii in range(len(items)):
                    artist = items[iii]

                    Distance = lev.distance(preprocessed_name, artist['name'].lower()),
                    Ratio = lev.ratio(preprocessed_name, artist['name'].lower())

                    if Ratio > 0.90:

                        spotify_match = True
                        print('Found fuzzy string match on index', iii, artist['name'])
                        print('with ratio:', Ratio)

                        artist_name_spotify = artist['name']
                        artist_img_spotify = artist['images'][0]['url']
                        artist_spotify_id = artist['id']
                        subgenres_spotify = artist['genres']
                        artist_popularity_spotify = artist['popularity']
                        break

                    else:
                        print('No fuzzy match on result from index ', iii, artist['name'])

        else:
            print('no Spotify search results at all from the preprocessed string')
    except:
        print('unsuccesful spotify lookup')

    return artist_name_spotify, artist_img_spotify, artist_spotify_id, subgenres_spotify, artist_popularity_spotify