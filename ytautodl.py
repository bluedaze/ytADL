# Guide for getting details from youtube videos for future reference.
# https://developers.google.com/youtube/v3/guides/implementation/videos
import requests
import datetime
import os
import subprocess
import argparse
from apikey import apikey
from errors import *

def validate_link():
	link = input("Please provide a link: ")
	try:
		requests.get(link)
		input_creaters(link)
	except requests.exceptions.MissingSchema:
		link_error()
		validate_link()
		print()

def input_creaters(link):
	try:
		upload_playlist = "UU" + link.split("/")[4][2::]
		print("\nThank you")
	except IndexError:
		yt_link_error()
		validate_link()
	else:
		return upload_playlist

def request_uploads(playlist_ID = None):
	if playlist_ID == None:
		''' Check the database '''
		pass
	else:
		data = {}
		playlist_ID = input_creaters()
		r = requests.get("https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=" + playlist_ID + "&key=" + apikey)
		print(r)
		response = r.json()["items"]
		for i in response:
			date = i["snippet"]["publishedAt"][0:10]
			videoID = i["snippet"]["resourceId"]["videoId"]
			data.update({date:videoID}) 
	return data

def download_video():
	today = datetime.datetime.now().isoformat()[0:10]
	ytprefix = "https://www.youtube.com/watch?v="
	uploads = request_uploads()
	for i in uploads:
		if i == today:
			download = ytprefix + uploads[i]
			print("Downloading " + download)
			fetch = subprocess.run(["youtube-dl", download], stdout=subprocess.DEVNULL)
			print("The exit code was: %d" % fetch.returncode)

		else:
			pass

def main():
	parser = argparse.ArgumentParser(description="Download Youtube Videos Automatically")

	parser.add_argument("-new", action='store_true', help="Add a youtube creator to the database.")

	args = parser.parse_args()

	if args.new:
		validate_link()
	else:
		pass




if __name__ == "__main__":
	main()