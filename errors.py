import sys
import time
import requests


def yt_link_error():
	notCorrectLink = '''\n\nThis is not the link we were looking for... 
	\nThis is Google's youtube account: https://www.youtube.com/channel/UCK8sQmJBp8GCxrOtXWBpyEA 
	\nThis is the kind of url we are looking for\n\n'''
	for c in notCorrectLink:
		sys.stdout.write(c)
		sys.stdout.flush()
		time.sleep(3./90)

def link_error():
	notCorrectLink = '''\n\nThis is not a valid link. Try again.\n\n'''
	for c in notCorrectLink:
		sys.stdout.write(c)
		sys.stdout.flush()
		time.sleep(3./90)