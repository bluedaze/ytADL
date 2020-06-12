# Guide for getting details from youtube videos for future reference.
# https://developers.google.com/youtube/v3/guides/implementation/videos
import requests
import subprocess
import argparse
from apikey import apikey
from validation import *

def main():
	parser = argparse.ArgumentParser(description="Download Youtube Videos Automatically")
	parser.add_argument("-new", action='store_true', help="Add a youtube creator to the database.")
	args = parser.parse_args()

	if args.new:
		# Only creates database and inserts new entry.
		url = User_data()
		create_db()
		request_uploads(url)
	# else:
	# 	request_uploads()
	# 	# download_video()

def request_uploads(playlist_id = None):
	link = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={playlist_id}&key={apikey}".format(playlist_id = playlist_id, apikey= apikey)
	r = requests.get(link)
	response = r.json()["items"]
	for i in response:
		channel_title = i["snippet"]["channelTitle"]
		channel_id = i["snippet"]["channelId"]
		uploads_id = i["snippet"]["playlistId"]
		video_id = i["snippet"]["resourceId"]["videoId"]
		video_date = i["snippet"]["publishedAt"][0:10]
		insert_data(channel_title, channel_id, uploads_id, video_id, video_date)

def download_video():
	# Downloads videos based upon video_id
	uploads = query_db()

	#TO DO: FIX THIS.

	# ytprefix = "https://www.youtube.com/watch?v="
	# for i in uploads:
	# 	download = ytprefix + uploads
	# 	print("Downloading " + download)
	# 	fetch = subprocess.run(["youtube-dl", download], stdout=subprocess.DEVNULL)
	# 	print("The exit code was: %d" % fetch.returncode)

if __name__ == "__main__":
	main()