# Guide for getting details from youtube videos for future reference.
# https://developers.google.com/youtube/v3/guides/implementation/videos
# TODO: Allow users to see which videos have been downloaded.
# TODO: Allow users to play video from terminal. Possibly use mplayer?
# TODO: Allow users to set what time task is scheduled. Unsure how to implement this. Crossplatform, so crontab may be out of the picture.
# TODO: Allow users to download videos from search.

# CHANGELOG: Sorta? idk? This is is what I am going to keep track of what has been changed.
# 1.) Refactored query_db() to return the same arguments every time.
# 2.) Refactored functions to correctly parse data returned from database.
# 3.) Added an argument so user can query database for a list of channels.
# 4.) Added ability to search youtube.

import requests
import subprocess
import argparse
from apikey import apikey
from validation import *
import os

def main():
	parser = argparse.ArgumentParser(description="Download Youtube Videos Automatically")
	parser.add_argument("-new", action='store_true', help="Add a youtube creator to the database.")
	parser.add_argument("-d", action='store_true', help="Checks database and downloads videos automatically")
	parser.add_argument("-channels", action='store_true', help="Shows you all channels that have been added to the database.")
	parser.add_argument("-search", action='store_true', help="Search youtube")
	args = parser.parse_args()

	if args.new:
		# Only creates database and inserts new entry.
		#TODO: Show confirmation messages which displays which channel was added to database.
		#TODO: Allow users to add channel by name.
		
		url = User_data()
		create_db()
		request_uploads(url)
	
	elif args.d:
		# Query the database, create a set of unique ids, send a request for each unique id.
		
		uploads = query_db()
		uid_set = set()

		for i in uploads:
			uid_set.add(i[2])
		for i in uid_set:
			request_uploads(i)

		download_video()

	elif args.search:
		search_results()

	elif args.channels:
		channel_set = set()
		data = query_db()

		for i in data:
			channel_set.add(i[0])
		for i in channel_set:
			print(i)
	else:
		print("You did not specify arguments. Type ytautodl.py -h for more information on how to run this program")

	#TODO: Create argument that will allow you to add from CSV.
	#TODO: Show related after videos are done downloading.

def request_uploads(playlist_id):
	#TODO: Skip videos which have been marked as downloaded.
	link = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=%s&key=%s" % (playlist_id, apikey)
	r = requests.get(link)
	response = r.json()["items"]
	for i in response:
		channel_title = i["snippet"]["channelTitle"]
		channel_id = i["snippet"]["channelId"]
		uploads_id = i["snippet"]["playlistId"]
		video_id = i["snippet"]["resourceId"]["videoId"]
		video_date = i["snippet"]["publishedAt"][0:10]
		video_title = i["snippet"]["title"]
		insert_data(channel_title, channel_id, uploads_id, video_id, video_date, video_title)

def search_results():
	videos = []
	search_query = input("Search: ")
	search_query  = search_query.replace(' ', '%20')
	linesep = "*------------------------------------------------------------------------------------------"
	link = "https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=5&q=%s&key=%s" % (search_query, apikey)
	print(link)
	r = requests.get(link)
	print(r)
	response = r.json()
	count = 0
	for i in response["items"]:
		count = count + 1
		channelTitle = i["snippet"]["channelTitle"]
		videoTitle = i["snippet"]["title"]
		description = i["snippet"]["description"]
		publishTime = i["snippet"]["publishTime"]
		try:
			video_id = i["id"]["videoId"]
			videos.append(video_id)
			print()
			print()
			print(linesep.replace("*", str(count)))
			print("| Channel:", channelTitle)
			print("| Video:", videoTitle)
			if description == "":
				print("| Description: None")
			else:
				print("| Description:", description)
			print("| Uploaded:", publishTime)
			print(linesep)
		except KeyError:
			count = count - 1
			pass

	print("totalResults:", response["pageInfo"]["totalResults"])
	print("resultsPerPage:", response["pageInfo"]["resultsPerPage"])
	choose_video = int(input("Enter a number to select which video you would like to see: "))
	choose_video = choose_video - 1
	print(choose_video)
	try:
		print("https://www.youtube.com/watch?v=" + videos[choose_video])
	except IndexError:
		print("Not a valid number")
	print(videos)

def download_video():
	today = datetime.datetime.now().isoformat()[0:10]
	uploads = query_db()
	ytprefix = "https://www.youtube.com/watch?v="
	for i in uploads:
		channel_title = i[0]
		video_id = i[3]
		video_date = i[4]
		video_title = i[5]
		path = os.getcwd() + "/" + channel_title
		download = ytprefix + video_id
		if os.path.isdir(path) == False:
				os.mkdir(path)
				print ("Directory %s created" % path)
		if video_date == today:
			os.chdir(path)
			print(os.getcwd())
			print("Downloading... \nChannel: %s \nVideo: %s \n%s" % (channel_title, video_title, download))
			fetch = subprocess.run(["youtube-dl", "-o", "%(uploader)s - %(title)s.%(ext)s", download], stdout=subprocess.DEVNULL)
			print("The exit code was: %d" % fetch.returncode)
			#TODO: If return code returns zero then marked as downloaded.
			os.chdir("..")

if __name__ == "__main__":
	main()