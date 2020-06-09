# Guide for getting details from youtube videos for future reference.
# https://developers.google.com/youtube/v3/guides/implementation/videos
import requests
import datetime
import os
import subprocess
import argparse
from apikey import apikey
from validation import *

def request_uploads(playlist_ID = None):
	data = {}
	if playlist_ID == None:
		''' Check the database '''
		pass
	else:
		r = requests.get("https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=" + playlist_ID + "&key=" + apikey)
		print(r)
		response = r.json()["items"]
		for i in response:
			date = i["snippet"]["publishedAt"][0:10]
			videoID = i["snippet"]["resourceId"]["videoId"]
			data.update({date:videoID}) 
	return data

def download_video(uploads):
	today = datetime.datetime.now().isoformat()[0:10]
	ytprefix = "https://www.youtube.com/watch?v="
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
		link = validate_link()
		playlist_id = input_creaters(link)
		todays_uploads = request_uploads(playlist_id)
		download_video(todays_uploads)

	else:
		pass

if __name__ == "__main__":
	main()