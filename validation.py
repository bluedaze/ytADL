import requests
import sys
import time

def input_validation():

	link = ""

	def link_error():
		error_message ='''\n\nThis is not the link we were looking for... 
						\nThis is Google's youtube account: https://www.youtube.com/channel/UCK8sQmJBp8GCxrOtXWBpyEA 
						\nThis is the kind of url we are looking for\n\n'''
		for c in error_message:
			sys.stdout.write(c)
			sys.stdout.flush()
			time.sleep(1/90)

	def validate_link():
		try:
			nonlocal link
			link = input("Please provide a link: ")
			r = requests.get(link)
		except requests.exceptions.MissingSchema:
			link_error()
			validate_link()
	
	def validate_yt():
		try:
			playlist_ID = "UU" + link.split("/")[4][2::]
		except IndexError:
			link_error()
		else:
			return playlist_ID

	return link

if __name__ == "__main__":
	input_validation()