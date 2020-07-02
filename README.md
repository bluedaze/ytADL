# ytADL
Automatically download content from youtube creators.

![Image of ytadl](https://i.imgur.com/j1yKqUE.gif)


ytADL is a wrapper around yt-download with sane defaults. It was designed first and foremost to automate downloads for your favorite channels and halfway through programming it I added several useful features.. I have found the tool to be great for archival purposes. You'll never have to worry about things like a DMCA takedown, or a channel removing content you missed again.

# Currently working options:
  -h, --help    show this help message and exit  
  -f F [F ...]  Set custom flags for youtube-dl.  
  -a            Add youtube api key. Only needed for search functionality. Would love a PR with a method that does not rely on youtube api.  
  -new          Add a new youtuber.  
  -d            Download new videos.  
  -c            Display channels stored in database.  
  -v            Display downloaded videos.  
  -search       Search youtube. Rerequires youtube api key.  
  -b            Send db info to txt file.  
  -silent       Run silently.  
