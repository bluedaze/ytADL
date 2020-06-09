# Guide for getting details from youtube videos for future reference.
# https://developers.google.com/youtube/v3/guides/implementation/videos
import requests
import datetime
import os
import subprocess
from apikey import apikey

today = datetime.datetime.now().isoformat()[0:10]
def request_uploads():
	data = {}
	r = requests.get("https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=UUBa659QWEk1AI4Tg--mrJ2A&key=" + apikey)
	print(r)
	response = r.json()["items"]
	for i in response:
		date = i["snippet"]["publishedAt"][0:10]
		videoID = i["snippet"]["resourceId"]["videoId"]
		data.update({date:videoID}) 
	return data

def download_video():
	youtube_dl = "https://www.youtube.com/watch?v="
	uploads = request_uploads()
	for i in uploads:
		if i == today:
			download = youtube_dl + uploads[i]
			print("Downloading " + download)
			list_files = subprocess.run(["youtube-dl", download], stdout=subprocess.DEVNULL)
			print("The exit code was: %d" % list_files.returncode)

		else:
			pass

download_video()