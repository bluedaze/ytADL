import requests
from errors import *

def validate_link():
	link = input("Please provide a link: ")
	try:
		requests.get(link)
	except requests.exceptions.MissingSchema:
		link_error()
		validate_link()
		print()
	else:
		print(link)
		return link

def input_creaters(link):
	try:
		playlist_ID = "UU" + link.split("/")[4][2::]
		print("\nThank you")
	except IndexError:
		yt_link_error()
		validate_link()
	else:
		return playlist_ID