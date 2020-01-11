from gmusicapi import Mobileclient

api = Mobileclient()
#api.perform_oauth()

# after running api.perform_oauth() once:
api.oauth_login(api.FROM_MAC_ADDRESS)

playlist = api.create_playlist("Google code in playlist", "Testing")
search = api.search("Insane In the Brain CYPRESS HILL")
songid = (search['station_hits'][0]['station']['seed']['trackId'])
api.add_songs_to_playlist(playlist, songid)