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
		error_message = "\n\nThis is not the link we were looking for... "
		error_message +="\n\nThis is Google's youtube account: https://www.youtube.com/channel/UCK8sQmJBp8GCxrOtXWBpyEA" 
		error_message +="\n\nThis is the kind of url we are looking for\n\n"

		for c in error_message:
			sys.stdout.write(c)
			sys.stdout.flush()
			time.sleep(.009)
		self.url = input("Please provide a link: ")
		self.validate_link(self.url)

	def validate_link(self, url):
		''' Validate if this is a url by sending a request to the url. '''
		regex = re.compile(r"(youtube.com/channel/UC)(.{22})")
		mo = regex.search(self.url)

		if mo == None:
			self.link_error()
		else:
			self.url = "UU" + mo.group()[22::]

	def __repr__(self):
		return "{self.__class__.__name__}({self.url})".format(self=self)

	def __str__(self):
		return "{self.url}".format(self=self)

if __name__ == "__main__":
	print(Validate("http://www.youtube.com/channel/UCK8sQmJBp8GCxrOtXWBpyEA"))