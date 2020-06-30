#!/usr/bin/env python
# Guide for getting details from youtube videos for future reference.
# https://developers.google.com/youtube/v3/guides/implementation/videos
# TODO: Allow users to play video from terminal. Possibly use mpv?
# TODO: Allow users to download videos from search.
# TODO: Show thumbnails in search.
# TODO: Allow users to add channel by name.
# TODO: Create argument that will allow you to add from CSV.
# TODO: Show related after videos are done downloading.
# TODO: Allow users to receive email notifcations.

# CHANGELOG: Sorta? idk? This is is what I am going to keep track of what has been changed.
# 1.) Removed old function request_uploads()
# 2.) Built framework for additional arguments, though some currently are not implemented entirely.
# 3.) Implemented function which shows you all videos that have been downloaded.
# 4.) Users may now specify their own youtube-dl functions.
# 5.) Adding a new youtuber now shows confirmation, and the name of the youtuber that was added.
# 6.) All flags are now moved to their own functions.
# 7.) Major reformat of code, now implemented Python black to reformat code.
# 8.) All important data can be backed up in a text file. Though I have not implemented a way to add data back to a database, yet. Ha!

import requests
import subprocess
import argparse
from apikey import apikey
from validation import *
import os
import feedparser
import time

color_green = "\u001b[38;5;46m"
stripformatting = "\u001b[0m"
underline = "\u001b[4m"
clearline = "\033[K"
moveup = "\033[1A"
movedown = "\033[1B"
returnhome = "\u001b[1000D"
bold = "\u001b[1m"
save = "\u001b[1s"
goback = "\u001b[1u"

ytadl = '''                                                                              
                                                                              
                     mm         db      `7MM"""Yb. `7MMF'                     
                     MM        ;MM:       MM    `Yb. MM                       
        `7M'   `MF'mmMMmm     ,V^MM.      MM     `Mb MM                       
          VA   ,V    MM      ,M  `MM      MM      MM MM                       
           VA ,V     MM      AbmmmqMA     MM     ,MP MM      ,                
            VVV      MM     A'     VML    MM    ,dP' MM     ,M                
            ,V       `Mbmo.AMA.   .AMMA..JMMmmmdP' .JMMmmmmMMM                
           ,V                              made by Sean Pedigo
         OOb                                                                   
                                                                              
'''


def main():

    parser = argparse.ArgumentParser(
        description="A wrapper for youtube-dl that adds additional features."
    )

    parser.add_argument(
        "-dp",
        action="store_true",
        help="Set default download path, else downloads in current location",
    )
    parser.add_argument(
        "-f", action="store", nargs="+", help="Set custome flags for youtube-dl",
    )
    parser.add_argument("-a", action="store_true", help="Add youtube api key")
    parser.add_argument("-new", action="store_true", help="Add a new youtuber.")
    parser.add_argument(
        "-d", action="store_true", help="Download new videos.",
    )
    parser.add_argument(
        "-c", action="store_true", help="Display channels stored in database.",
    )
    parser.add_argument("-p", action="store_true", help="List your preferences")
    parser.add_argument(
        "-v", action="store_true", help="Display downloaded videos",
    )
    parser.add_argument("-search", action="store_true", help="Search youtube")
    parser.add_argument("-b", action="store_true", help="Send db info to txt file.")
    parser.add_argument(
        "-silent", action="store_true", help="Run without print to the cli."
    )
    parser.add_argument(
        "-ep", action="store_true", help="enable plex, and set plex options"
    )
    args = parser.parse_args()

    if args.new:
        new()

    elif args.d:
        download_video()

    elif args.search:
        search_results()

    elif args.c:
        channels()

    elif args.p:
        pass

    elif args.v:
        videos()

    elif args.f:
        download_video(args.f)
    elif args.b:
        backup_query()

    else:
        print(
            f"{color_green} You did not specify arguments. Type ytautodl.py -h for more information on how to run this program\n{stripformatting}"
        )


def new():
    # Only creates database and inserts new entry.

    url = User_data()
    create_db()
    # Returns details from the feed. Currently only returns youtube name.
    details = parse_ytrss(url)

    print(f"\n\n\n\t{details} added to database")


def channels():
    print(f"{underline} {color_green} Your Channels: {stripformatting}")
    channel_set = set()
    data = query_db()

    for i in data:
        channel_set.add(i[0])
    for i in channel_set:
        print(f"{color_green} {i} {stripformatting}\n\n")


def videos():
    videos = []
    data = query_videos()
    for i in data:
        channel = i[0].ljust(40)
        video = i[2].ljust(40)
        entry = channel + video
        videos.append(entry)
    mylist = videos.sort()
    for i in videos:
        print(i)


def parse_ytrss(rss_link):
    """ Fetch rss feed from youtube, and parse feed to look for new videos """
    rss_link = f"https://www.youtube.com/feeds/videos.xml?channel_id={rss_link}"

    r = requests.get(rss_link)
    page = r.text

    d = feedparser.parse(page)
    entries = d.entries

    for i in entries:
        channel_title = i["authors"][0]["name"]
        channel_id = i["yt_channelid"]
        uploads_id = f"{'UU'}{channel_id[2::]}"
        video_id = i["yt_videoid"]
        video_date = i["published"][0:10]
        video_title = i["title"]
        description = i["summary"]
        downloaded = "0"
        insert_data(
            channel_title,
            channel_id,
            uploads_id,
            video_id,
            video_date,
            video_title,
            description,
            downloaded,
        )

    return channel_title


def search_results():
    """ Uses Google api to search, must supply your own api key """
    videos = []
    search_query = input("Search: ")
    search_query = search_query.replace(" ", "%20")
    linesep = f"*{'-'*90}"
    params = {"part": "snippet", "maxResults": 5, "q": search_query, "key": api_key}
    link = "https://www.googleapis.com/youtube/v3/search"
    r = requests.get(link, params=params)
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
            print("\n\n")
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
            count -= 1
            pass

    print("totalResults:", response["pageInfo"]["totalResults"])
    print("resultsPerPage:", response["pageInfo"]["resultsPerPage"])
    choose_video = int(
        input("Enter a number to select which video you would like to see: ")
    )
    choose_video -= 1
    print(choose_video)
    try:
        print(f"https://www.youtube.com/watch?v={videos[choose_video]}")
    except IndexError:
        print("Not a valid number")
    print(videos)


def download_video(ytargs=None):
    """ Fetches videos marked as not downloaded, and downloads them """

    print(f"{color_green}Searching for content...{stripformatting}")

    youtubers = query_creators()
    uid_set = set()

    for i in youtubers:
        uid_set.add(i[1])
    for i in uid_set:
        parse_ytrss(i)
    # Initialize variable channel. Will be used to prevent reprints of name of channel to the console
    channelName = ""
    uploads = query_db()
    for i in uploads:
        channel_title = i[0]
        video_id = i[3]
        video_date = i[4]
        video_title = i[5]
        path = f"{os.getcwd()}{'/'}{channel_title}"
        download = f"https://www.youtube.com/watch?v={video_id}"
        if os.path.isdir(path) == False:
            os.mkdir(path)
            print(f"Directory {path} created")

        os.chdir(path)
        if channelName != channel_title:
            channelName = channel_title
            print(
                f"{moveup}{returnhome}{clearline}{color_green}Channel: {bold}{channel_title}{stripformatting}"
            )
        print(
            f"{returnhome}{clearline}{color_green}Video: {video_title}{stripformatting}",
            end="",
        )
        sys.stdout.flush()

        flags = [
            "youtube-dl",
            "--no-warnings",
            "-i",
            "-o",
            "%(uploader)s - %(title)s.%(ext)s",
            "--external-downloader",
            "aria2c",
            "--external-downloader-args",
            "'-x 8 -s 8 -k 1m'",
            download,
        ]

        if ytargs is None:
            pass
        else:
            flags = ytargs

        fetch = subprocess.run(flags, stdout=subprocess.DEVNULL,)
        os.chdir("..")

        if fetch.returncode == 0:
            mark_downloaded(video_id)


if __name__ == "__main__":
    print(f"{color_green} {ytadl} {stripformatting}")
    main()
    print(f"{color_green}\n\nThank you for using ytautodl...{stripformatting}\n\n")
