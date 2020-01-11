from bs4 import BeautifulSoup
import string
import requests
from gmusicapi import Mobileclient


songs = []
api = Mobileclient()

""" Adds the song to the playlist """
def add_to_playlist(title, authors):
	#print(title)
	#print("     " + authors[0])
	search_term = title + " " + authors[0]
	print("Search Term: " + search_term)
	search = api.search(search_term) # Looks for the matching song in the GPM store

	songid = ""

	try:
		songid = search['song_hits'][0]['track']['storeId']
		print("    Song ID: " + songid + "\n")
	except:
		try:
			songid = search['song_hits'][0]['track']['albumId']
			print("    Album ID: " + songid + "\n")
		except:
			try:
				songid = search['station_hits'][0]['station']['seed']['trackId']
				print("    Track ID: " + songid + "\n")
			except:
				pass


	if (songid != ""):
		songs.append(songid)

""" Parse through all the links until you get to a song """
def search_recursive(elem, i=1, url=""):

	# If this is the first time the function is called
	# Decide what type of page it is (e.g. movie, song, show, game, etc)
	if elem == None:

		# Isolate parts of the url
		split = url.split("/")

		# Checks the url to see if this web page is for a show
		if split[-3] == "show":
			print("show")
			search_recursive("show", 1, url)
		# Checks the url to see if this web page is for a movie
		elif split[-3] == "movie":
			print("movie")
			search_recursive("movie", url=url)
		# Checks the url to see if this web page is for a game
		elif split[-3] == "game":
			print("game")
			search_recursive("game", url=url)

	elif elem == "show":
		# Do some magic using Beautiful Soup
		# Obtains html page from url
		html = BeautifulSoup(requests.get((url + "season-" + str(i))).text, 'html.parser')
		
		# This means that there are no more season in the show
		if "Page not found" in html.find_all('h2')[0]:
			#print("Page not found")
			return

		soup = html.find_all('a')
		# Searches for episodes for each season of the show
		for spoon in soup:
			if "#song" in spoon['href']:
				search_recursive("song", url="https://www.tunefind.com"+ spoon['href'])

		search_recursive("show", i + 1, url)

	elif elem == "song" or elem == "movie" or elem=="game":
		#print(url)
		# Do some magic using Beautiful Soup
		# Obtains html page from url
		html = BeautifulSoup(requests.get(url).text, 'html.parser')
		soup = html.find_all('a')

		# Searches for a song for every episode
		title = ""
		artists = []

		# For every song, get the title and artist
		# TODO: Support more than one artist per song
		for i in range(len(soup)):
			spoon = soup[i]

			if "/song/" in spoon['href']:
				title = spoon.text
				if (i < len(soup) - 1) and ("/artist/" in soup[i+1]['href']):
			 		artists.append(soup[i+1].text)
			 		continue

			elif (title != "" and artists != []):
				add_to_playlist(title, artists)
				artists.clear()
				title = ""


def main():

	""" Test Cases """
	link = "https://www.tunefind.com/game/john-wick-hex-2019"
	playlist_title = "John Wick"
	description = ""

	link = "https://www.tunefind.com/movie/catch-me-if-you-can-2002"
	playlist_title = "Catch Me If You Can (2002)"
	description = ""

	link = "https://www.tunefind.com/show/mr-robot/"
	playlist_title = "Mr. Robot"
	description = ""


	#link = input("Input the tunefind.com url: ")
	#playlist_title = input("What do you want to call your Google Play Music Playlist?: ")
	#description = input("[Optional] Add a description for your playlist (Press enter if you want to leave this blank): ")

	# Remove whitespace and new lines
	link = link.translate({ord(c): None for c in string.whitespace})
	# If the url doesn't have trailing / at the end, add it 
	if link[-1] != '/':
		link += '/'

	""" Do GPM API Stuff"""
	 	#api.perform_oauth()
	# after running api.perform_oauth() once:
	api.oauth_login(api.FROM_MAC_ADDRESS)
	playlist = api.create_playlist(playlist_title, description)

	print("Loading tunefind.com page...")
	search_recursive(None, url=link)

	api.add_songs_to_playlist(playlist, songs)

if __name__ == "__main__":
    main()
