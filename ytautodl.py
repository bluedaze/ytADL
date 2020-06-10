# Guide for getting details from youtube videos for future reference.
# https://developers.google.com/youtube/v3/guides/implementation/videos
import requests
import datetime
import subprocess
import argparse
from apikey import apikey
from validation import Validate
import sqlite3

def request_uploads(playlist_ID = None):
	data = {}
	if playlist_ID == None:
		''' Check the database '''
		pass
	else:
		link = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={playlist_ID}&key={apikey}".format(playlist_ID = playlist_ID, apikey= apikey)
		r = requests.get(link)
		response = r.json()["items"]
		for i in response:
			date = i["snippet"]["publishedAt"][0:10]
			videoID = i["snippet"]["resourceId"]["videoId"]
			channelTitle = i["snippet"]["channelTitle"]
			playlistId = i["snippet"]["playlistId"]
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

def new_channel():
	link = input("Please provide a link: ")
	playlist_ID = Validate(link)
	todays_uploads = request_uploads(playlist_ID)
	download_video(todays_uploads)

	# TODO:
	# Implement database



def create_database():

	table_sql = "CREATE TABLE IF NOT EXISTS tweets (youtuber_url TEXT, uploads_url TEXT, youtuber TEXT)"

	conn = sqlite3.connect('yt.db')
	c = conn.cursor()
	c.execute(table_sql)
	c.close()
	conn.close()

def main():
	parser = argparse.ArgumentParser(description="Download Youtube Videos Automatically")
	parser.add_argument("-new", action='store_true', help="Add a youtube creator to the database.")
	args = parser.parse_args()

	if args.new:
		new_channel()
	else:
		''' Check creators in database '''
		pass

if __name__ == "__main__":
	main()