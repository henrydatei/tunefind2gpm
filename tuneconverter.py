from bs4 import BeautifulSoup
import string
import requests
from gmusicapi import Mobileclient


songs = []
api = Mobileclient()

""" Adds the song to the playlist """
def add_to_playlist(title, authors):
	print(title)
	print("     " + str(authors))

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
			#search_recursive("movie", 1)
		# Checks the url to see if this web page is for a game
		elif split[-3] == "game":
			print("game")
			#search_recursive("game", 1)

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

	elif elem == "song":
		#print(url)
		# Do some magic using Beautiful Soup
		# Obtains html page from url
		html = BeautifulSoup(requests.get(url).text, 'html.parser')
		soup = html.find_all('a')

		# Searches for a song for every episode
		title = ""
		artists = []
		for spoon in soup:
			if "/song/" in spoon['href']:
				if (title != "" and artists != []):
					add_to_playlist(title, artists)
				artists = []
				title = spoon.text
			if "/artist/" in spoon['href']:
				artists.append(spoon.text)

		add_to_playlist(title, artists)


def main():

	link = "https://www.tunefind.com/show/mr-robot"
	playlist_title = "Mr. Robot"
	description = "All the songs from Mr. Robot"
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



if __name__ == "__main__":
    main()

#soup = BeautifulSoup(open(link).read())