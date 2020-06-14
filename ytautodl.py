# Guide for getting details from youtube videos for future reference.
# https://developers.google.com/youtube/v3/guides/implementation/videos
import requests
import subprocess
import argparse
from apikey import apikey
from validation import *
import os

def main():
	parser = argparse.ArgumentParser(description="Download Youtube Videos Automatically")
	parser.add_argument("-new", action='store_true', help="Add a youtube creator to the database.")
	parser.add_argument("-d", action='store_true', help="Default argument. Checks database and downloads videos automatically")
	args = parser.parse_args()

	if args.new:
		# Only creates database and inserts new entry.
		url = User_data()
		create_db()
		request_uploads(url)
	elif args.d:
		uploads = query_db(distinct = "distinct")
		for i in uploads:
			request_uploads(i[1])
		download_video()
	else:
		print("You did not specify arguments. Type ytautodl.py -h for more information on how to run this program")

def request_uploads(playlist_id):
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
	today = datetime.datetime.now().isoformat()[0:10]
	#TO DO: Need function to organize content into folders based on channel name.
	uploads = query_db()
	ytprefix = "https://www.youtube.com/watch?v="
	for i in uploads:
		channel_title = i[0]
		video_id = i[1]
		video_date = i[2]
		path = "./" + channel_title
		download = ytprefix + video_id
		if video_date == today:
			if os.path.isdir(path) == False:
				try:
					os.mkdir(path)
				except OSError:
					print ("Creation of the directory %s failed" % path)
				else:
					print ("Successfully created the directory %s " % path)
			os.chdir(path)
			print("Downloading " + channel_title + " " + download + " " + video_date)
			fetch = subprocess.run(["youtube-dl", download], stdout=subprocess.DEVNULL)
			# print("The exit code was: %d" % fetch.returncode)
			os.chdir("..")

if __name__ == "__main__":
	main()