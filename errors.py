import sys
import time


def yt_link_error():
	error_message = '''\n\nThis is not the link we were looking for... 
	\nThis is Google's youtube account: https://www.youtube.com/channel/UCK8sQmJBp8GCxrOtXWBpyEA 
	\nThis is the kind of url we are looking for\n\n'''
	for c in error_message:
		sys.stdout.write(c)
		sys.stdout.flush()
		time.sleep(3./90)

def link_error():
	error_message = '''\n\nThis is not a valid link. Try again.\n\n'''
	for c in error_message:
		sys.stdout.write(c)
		sys.stdout.flush()
		time.sleep(3./90)