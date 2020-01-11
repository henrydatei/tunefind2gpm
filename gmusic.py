from gmusicapi import Mobileclient

api = Mobileclient()
#api.perform_oauth()

# after running api.perform_oauth() once:
api.oauth_login(api.FROM_MAC_ADDRESS)

playlist = api.create_playlist("Google code in playlist", "Testing")
search = api.search("mr. roboto styx")
songid = search['song_hits'][0]['track']['storeId']
print(songid)
api.add_songs_to_playlist(playlist, songid)