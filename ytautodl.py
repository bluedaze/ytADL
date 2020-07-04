#!/usr/bin/env python
# Guide for getting details from youtube videos for future reference.
# https://developers.google.com/youtube/v3/guides/implementation/videos
# TODO: Allow users to play video from terminal. Possibly use mpv?
# TODO: ~Allow users to download videos from search.
# TODO: ~Show thumbnails in search.
# TODO: ~Allow users to add channel by name.
# TODO: Create argument that will allow you to add from CSV.
# TODO: ~Show related after videos are done downloading.
# TODO: Add plex options
# TODO: Change flags. Examples ytadl list, ytadl search foo, ytadl config set api_key.. ytadl play --mpv
# TODO: Make all flags work.
# TODO: Add a filter for time.
# TODO: Embed thumbnails in videos.

# CHANGELOG: Sorta? idk? This is is what I am going to keep track of what has been changed.
# 1.) Added threading for parsing youtube feeds. Significant improvement fetch times, which was the slowest part of the program.
# 2.) Had to update new() to be useful after refactoring parse_ytrss
# 3.) Started on MPV function.
# 4.) Refactored how ansi escape sequences are printed to make it more logical.
# 5.) Refactored SQL functions. Data is not fetched immediately when the program is started, and flags filter prefetched data
# according to user needs.
# 6.)
# 7.)
# 8.)

#Flags to change: 
# -a
# -c
# -f

from rich import print
from rich.panel import Panel
from rich.console import Console
from rich.table import Column, Table
import requests
import subprocess
import argparse
# from apikey import apikey
from validation import *
from utils import *
import os
import feedparser
import time
import logging
import threading
try:
    from apikey import apikey
except ModuleNotFoundError:
    missingApi = '''You are missing an API key. 
If you want to use the search function please provide it'''
searchVar = 0
from sqlfunc import *

obj = Information()
ytadl = '''[bold green]                                                                              
                                                                              
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
        "-f", action="store", nargs="+", help="Set custom flags for youtube-dl.",
    )
    parser.add_argument(
        "-a",
        action="store_true",
        help="Add youtube api key. Only needed for search functionality. Would love a PR with a method that does not rely on youtube api.",
    )
    parser.add_argument("-new", action="store_true", help="Add a new youtuber.")
    parser.add_argument(
        "-d", action="store_true", help="Download new videos.",
    )
    parser.add_argument(
        "-c", action="store_true", help="Display channels stored in database.",
    )
    parser.add_argument("-p", action="store_true", help="List your preferences.")
    parser.add_argument(
        "-v", action="store_true", help="Display downloaded videos.",
    )
    parser.add_argument(
        "-search",
        action="store_true",
        help="Search youtube. Rerequires youtube api key.",
    )
    parser.add_argument("-pv", action="store_true", help="Play a video using mpv.")
    parser.add_argument("-b", action="store_true", help="Send db info to txt file.")
    parser.add_argument("-silent", action="store_true", help="Run silently.")
    parser.add_argument(
        "-ep", action="store_true", help="enable plex, and set plex options"
    )
    args = parser.parse_args()

    if args.silent:
        log_mode = logging.basicConfig(level=logging.CRITICAL, format="")
    else:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler(sys.stdout)
        handler.terminator = ""
        handler.setLevel(logging.INFO)

        formatter = logging.Formatter("")
        handler.setFormatter(formatter)

        console = Console()
        logger.addHandler(handler)
        console.print(Panel(ytadl), width=100)

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

    elif args.pv:
        play_video()


# def play_video():
#     my_channels = channels()
#     obj = enumerate(my_channels, start=1)
#     for count, i in obj:
#         print(str(count) + ": " + str(i))


def new():
    """ Fetch rss feed from youtube, and parse feed to look for new videos """
    url = User_data()
    logging.debug(f"User entered: {url}")
    rss_link = f"https://www.youtube.com/feeds/videos.xml?channel_id={url}"

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
    logging.info(f"\n\n\n\t{channel_title} added to database")


def channels():
    '''
    Returns a unique list of channels and display them to the terminal
    '''
    channels = obj.channels()
    display = obj.display(channels, "Channels")


def videos():
    '''
    Display all videos that have been downloaded to the terminal
    '''
    videos = obj.videos()
    display = obj.display(videos, "Videos")


def parse_ytrss():
    """ Fetch rss feed from youtube, and parse feed to look for new videos """
    # List of dictionaries for entries
    youtubers = obj.query_db()
    uid_set = set()

    for i in youtubers:
        uid_set.add(i[1])

    rss_entries = []

    def fetch_feed(uid):
        rss_link = f"https://www.youtube.com/feeds/videos.xml?channel_id={uid}"

        # Move to seperate function blow this.
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

            d = {
                "channel_title": channel_title,
                "channel_id": channel_id,
                "uploads_id": uploads_id,
                "video_id": video_id,
                "video_date": video_date,
                "video_title": video_title,
                "description": description,
                "downloaded": downloaded,
            }
            rss_entries.append(d)
            # Append to dictionary with this function.

    threads = []
    for i in uid_set:
        t = threading.Thread(target=fetch_feed, args=[i])
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()

    # Create seperate function.
    for i in rss_entries:
        channel_title = i["channel_title"]
        channel_id = i["channel_id"]
        uploads_id = i["uploads_id"]
        video_id = i["video_id"]
        video_date = i["video_date"]
        video_title = i["video_title"]
        description = i["description"]
        downloaded = i["downloaded"]
        obj.insert_data(
            channel_title,
            channel_id,
            uploads_id,
            video_id,
            video_date,
            video_title,
            description,
            downloaded,
        )

def search_results():
    """ Uses Google api to search, must supply your own api key """
    if searchVar == 0:
        print(missingApi)
        pass
    else:
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
                logging.info("\n\n")
                logging.info(linesep.replace("*", str(count)))
                logging.info("| Channel:", channelTitle)
                logging.info("| Video:", videoTitle)
                if description == "":
                    logging.info("| Description: None")
                else:
                    logging.info("| Description:", description)
                logging.info("| Uploaded:", publishTime)
                logging.info(linesep)
            except KeyError:
                count -= 1
                pass

        logging.info("totalResults:", response["pageInfo"]["totalResults"])
        logging.info("resultsPerPage:", response["pageInfo"]["resultsPerPage"])
        choose_video = int(
            input("Enter a number to select which video you would like to see: ")
        )
        choose_video -= 1
        logging.info(choose_video)
        try:
            logging.info(f"https://www.youtube.com/watch?v={videos[choose_video]}")
        except IndexError:
            logging.info("Not a valid number")
        logging.info(videos)


def download_video(ytargs=None):
    """ Fetches videos marked as not downloaded, and downloads them """

    logging.info(color("Searching for content...\n", text_color="matrix"))

    parse_ytrss()
    # Initialize variable channel. Will be used to prevent relogging.infos of name of channel to the console
    channelName = ""
    data = obj.in_queue()
    for i in data:
        channel_title = i['channel_title']
        video_id = i["video_id"]
        video_date = i["video_date"]
        video_title = i["video_title"]
        path = f"{os.getcwd()}{'/'}{channel_title}"
        download = f"https://www.youtube.com/watch?v={video_id}"

        if os.path.isdir(path) == False:
            os.mkdir(path)
            logging.info(f"Directory {path} created")
        os.chdir(path)

        if channelName != channel_title:
            channelName = channel_title
            logging.info(
                color(
                    f"\r{up}{clearline}Channel:{bold(channel_title)}\n",
                    text_color="matrix",
                )
            )
        logging.info(color(f"\r{clearline}Video:{video_title}", text_color="matrix"))
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

        fetch = subprocess.run(flags, stdout=subprocess.DEVNULL)

        os.chdir("..")

        if fetch.returncode == 0:
            obj.mark_downloaded(video_id)
        elif fetch.returncode == 1:
            print("{channel_title} - {video_title} did not download.")


if __name__ == "__main__":
    os.system("setterm -cursor off")
    main()
    os.system("setterm -cursor on")
    logging.info(color("\n\nThank you for using ytautodl...\n\n", text_color="matrix"))
