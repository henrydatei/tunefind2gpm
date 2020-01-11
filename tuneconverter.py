from bs4 import BeautifulSoup
import string
import requests

link = "https://www.tunefind.com/show/derry-girls/"

songs = []

""" Adds the song to the playlist """
def add_to_playlist(title, author):
	pass

""" Parse through all the links until you get to a song """
def search_recursive(elem, i=1, url=""):

	# If this is the first time the function is called
	# Decide what type of page it is (e.g. movie, song, show, game, etc)
	if elem == None:

		elem = link

		# Remove whitespace and new lines
		elem = elem.translate({ord(c): None for c in string.whitespace})

		# If the url doesn't have trailing / at the end, add it 
		if elem[-1] != '/':
			elem = elem[:-1]

		# Isolate parts of the url
		elem = elem.split("/")

		# Checks the url to see if this web page is for a show
		if elem[-3] == "show":
			print("show")
			search_recursive("show", 1)
		# Checks the url to see if this web page is for a movie
		elif elem[-3] == "movie":
			print("movie")
			#search_recursive("movie", 1)
		# Checks the url to see if this web page is for a game
		elif elem[-3] == "game":
			print("game")
			#search_recursive("game", 1)

	elif elem == "show":
		# Do some magic using Beautiful Soup
		# Obtains html page from url
		html = BeautifulSoup(requests.get((link + "season-" + str(i))).text, 'html.parser')
		
		# This means that there are no more season in the show
		if "Page not found" in html.find_all('h2')[0]:
			print("Page not found")
			return

		soup = html.find_all('a')
		# Searches for episodes for each season of the show
		for spoon in soup:
			if "#song" in spoon['href']:
				search_recursive("song", url=spoon['href'])

		search_recursive("show", i + 1)

	elif elem == "song":
		print(url)
		
		


def main():
	
	print("Loading tunefind.com page...")

	search_recursive(None)



if __name__ == "__main__":
    main()

#soup = BeautifulSoup(open(link).read())