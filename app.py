import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials())

all_data = []


def main():

    playlist_urls = pd.read_csv("data/sleepy_lofi_playlists.csv")
    for playlist_url in playlist_urls["URL"]:
        playlist_uri = playlist_url.split("/")[-1].split("?")[0]
        playlist_tracks = spotify.playlist_tracks(playlist_uri)["items"]

        for track in playlist_tracks:
            artist_name = track["track"]["artists"][0]["name"]
            track_name = track["track"]["name"]
            album_name = track["track"]["album"]["name"]
            artist_link = track["track"]["artists"][0]["external_urls"]["spotify"]
            track_link = track["track"]["external_urls"]["spotify"]
            album_link = track["track"]["album"]["external_urls"]["spotify"]
            release_date = track["track"]["album"]["release_date"]
            popularity = track["track"]["popularity"]
            track_uri = track["track"]["uri"]
            artist_uri = track["track"]["artists"][0]["uri"]
            album_uri = track["track"]["album"]["uri"]

            audio_features = spotify.audio_features(track_uri)
            for feature in audio_features:
                try:
                    duration_ms = feature["duration_ms"]
                except:
                    duration_ms = None
                if duration_ms != None:
                    duration_mins = float(duration_ms) / 60000
                    duration = "{:.2f}".format(duration_mins)
                try:
                    tempo = round(feature["tempo"])
                except:
                    tempo = None
                try:
                    loudness = round(feature["loudness"])
                except:
                    loudness = None
                try:
                    time_sig = round(feature["time_signature"])
                except:
                    time_sig = None
                try:
                    key_sig = feature["key"]
                except:
                    key_sig = None
                if key_sig != None:
                    match key_sig:
                        case -1:
                            key_sig = "None"
                        case 0:
                            key_sig = "C"
                        case 1:
                            key_sig = "C#/Db"
                        case 2:
                            key_sig = "D"
                        case 3:
                            key_sig = "D#/Eb"
                        case 4:
                            key_sig = "E"
                        case 5:
                            key_sig = "F"
                        case 6:
                            key_sig = "F#/Gb"
                        case 7:
                            key_sig = "G"
                        case 8:
                            key_sig = "G#/Ab"
                        case 9:
                            key_sig = "A"
                        case 10:
                            key_sig = "A#/Bb"
                        case 11:
                            key_sig = "B"
                try:
                    modality = feature["mode"]
                except:
                    modality = None
                if modality == 1:
                    modality = "Major"
                else:
                    modality = "minor"
                try:
                    acousticness = feature["acousticness"]
                except:
                    acousticness = None
                try:
                    positiveness = feature["valence"]
                except:
                    positiveness = None
                try:
                    energy = feature["energy"]
                except:
                    energy = None

            all_data.append((artist_name, track_name, album_name, duration, popularity, tempo, time_sig, key_sig,
                             modality, energy, loudness, acousticness, positiveness, release_date, artist_link, album_link, track_link, artist_uri, album_uri, track_uri))

        df = pd.DataFrame(all_data, columns=["Artist Name", "Track Name", "Album Name", "Duration", "Popularity", "Tempo", "Time Sig", "Key", "Modality", "Energy",
                                             "Loudness", "Acousticness", "Positiveness", "Release Date", "Artist Link", "Album Link", "Track Link", "Artist URI", "Album URI", "Track URI"])
        df.to_csv("data/track_data.csv", index=True)


if __name__ == "__main__":
    main()
