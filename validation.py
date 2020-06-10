import requests
import sys
import time
import re

class Validate:
	''' Checks for valid youtube link '''
	def __init__(self, url):
		self.url = url
		self.validate_link(self.url)

	def link_error(self):
		''' Error message for invalid link. '''
		error_message ='''\n\nThis is not the link we were looking for... 
						\nThis is Google's youtube account: https://www.youtube.com/channel/UCK8sQmJBp8GCxrOtXWBpyEA 
						\nThis is the kind of url we are looking for\n\n'''
		for c in error_message:
			sys.stdout.write(c)
			sys.stdout.flush()
			time.sleep(.009)
		self.url = input("Please provide a link: ")
		self.validate_link(self.url)

	def validate_link(self, url):
		''' Validate if this is a url by sending a request to the url. '''
		try:
			r = requests.get(self.url)
		except requests.exceptions.MissingSchema:
			self.link_error()
			self.validate_link()
		else:
			# Calls validate_yt(), and returns the value if there is no error.
			return self.validate_yt()
	
	def validate_yt(self):
		''' Parse url to check if this is a valid youtube link. '''
		try:
			self.url = "UU" + self.url.split("/")[4][2::]
		except IndexError:
			self.link_error()

	def __repr__(self):
		return "{self.__class__.__name__}({self.url})".format(self=self)

	def __str__(self):
		return "{self.url}".format(self=self)

if __name__ == "__main__":
	print(Validate("https://www.youtube.com/channel/UCK8sQmJBp8GCxrOtXWBpyEA"))