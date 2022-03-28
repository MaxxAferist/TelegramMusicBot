import lyricsgenius as lg
from tokens import GENIUS_TOKEN
import json
import os


genius = lg.Genius(GENIUS_TOKEN)
song = genius.search_song('В питере пить')
filename = f'lyrics_{song.artist}_{song.title}.json'.lower()
song.save_lyrics(filename)
with open(filename) as file:
    json_song = json.loads(file.read())
print(json_song)