from posixpath import split
import spotipy
import spotipy.util as util
from datetime import date
import random

from flask import Flask, render_template, request, redirect

client_id = '2e8136a186b8455f8d5a7b443896a69d'
client_seccret = 'a48e774a2e8042eb9e2b81550d71565a'
redirect_uri ='https://github.com/hkowthee'

scope = 'user-library-read user-top-read playlist-modify-public user-follow-read'

username = 'Harishvar'

token = util.prompt_for_user_token(username, scope, client_id, client_seccret, redirect_uri)


def onefunction(mood):

    print(mood)

    #Authenticating spotify
    sp = spotipy.Spotify(auth=token)
    print("authenticating spotify-------------done")

    #getting the followed and viewed artists of the user
    uris = set()

    #backup to add more artist
    #names = set()

    viewed_artists = sp.current_user_top_artists(limit=20)
    followed_artists = sp.current_user_followed_artists(limit=20)
    followed = followed_artists['artists']

    for top in viewed_artists['items']:
        uris.add(top['uri'])
        #names.add(top["name"])

    for eachfollwed in followed['items']:
        uris.add(eachfollwed['uri'])
        #names.add(eachfollowed["name"])

    print("getting all the artists---------done")

    #check =set()
    #check = uris.copy()
    #for artist_uri in check:
    #    artist_related = sp.artist_related_artists(artist_uri)
    #    artist_data = artist_related['artists']
    #    stop = 0

    #    for artist in artist_data:
    #        print("k")
    #        uris.add(artist['uri])
    #        names.add(artist['name'])
    #        if stop == 5:
    #            break
    #        stop = stop + 1


    #getting all the top songs of the artists we have collected before 
    allSongs_uri = []
    for artist in uris:
        topSongs = sp.artist_top_tracks(artist)
        #print(topSongs)
        for song_uri in topSongs['tracks']:
            #print(Song)
            allSongs_uri.append(song_uri['uri'])

    print(len(allSongs_uri))

    print("getting top songs of all the artists-----done")


    #separate songs based on moood
    random.shuffle(allSongs_uri)
    finalsongs = []

    for song_uri in allSongs_uri:
        allSongs = sp.audio_features(song_uri)
        #print(allSongs)
        #print(len(allSongs))
        for song in allSongs:
            #print(song['valance'])
            try:
                if mood == 'Feel':
                    if(0 <= song['valence'] <=0.25):
                        finalsongs.append(song['uri'])
                elif mood == 'Flow':
                    if(0.25 < song['valence'] <=0.5):
                        finalsongs.append(song['uri'])
                elif mood =='Forward':
                    if(0.5 < song['valence'] <=0.75):
                        finalsongs.append(song['uri'])
                elif mood == 'Energy':
                    if(0.75 < song['valence'] <=1.0):
                        finalsongs.append(song['uri'])
            except:
                continue
    random.shuffle(finalsongs)
    print(len(finalsongs))
    print("seperating the songs based on mood--------done")


    #create playlist for the user
    today = date.today()
    user = sp.current_user()
    playlist = sp.user_playlist_create(user['id'], "SoulMusic " + mood + " " + str(today))
    sp.user_playlist_add_tracks(user['id'], playlist['id'],finalsongs[0:50])
    #print(playlist)
    print("creating a playlist and adding-------done")
    return playlist

app = Flask(__name__)

@app.route('/')
def mainpage():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def SoulMusic():
    mood = request.form['songs']
    playlist = onefunction(mood)
    #print(playlist)
    playlist_loc1 = playlist['external_urls']
    playlist_final = playlist_loc1['spotify']
    split = playlist_final.split('playlist')
    print(split[0])
    print(split[1])
    album = split[1]
    return render_template('songs.html', album = album)

if __name__ == "__main__":
    app.run(host ='0.0.0.0', debug=True)
