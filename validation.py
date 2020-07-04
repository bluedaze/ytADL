import sys
import time
import re
import datetime
import sqlite3


class User_data:
    """ Checks for valid youtube link """

    def __init__(self):
        self.url = ""
        self.user_link(self.url)

    def __str__(self):
        return "{self.url}".format(self=self)

    def user_link(self, url):
        """ Error message for invalid link. """
        message = """To create an entry we need the channel url.
		\n\nHere is an example using Google's youtube channel: https://www.youtube.com/channel/UCK8sQmJBp8GCxrOtXWBpyEA"""

        for c in message:
            sys.stdout.write(c)
            sys.stdout.flush()
            time.sleep(0.009)
        self.url = input("\n\nPlease provide a similar link: ")
        self.validate_link()

    def validate_link(self):
        """ Validate if this is a url by sending a request to the url. """
        regex = re.compile(r"(youtube.com/channel/UC)(.{22})")
        mo = regex.search(self.url)

        if mo == None:
            print("~~~~~~~~~~~~~~~\n\n\nThat is not the link we are looking for.\n")
            self.user_link(self.url)
        else:
            # https://www.youtube.com/feeds/videos.xml?channel_id=UCuXy5tCgEninup9cGplbiFw
            self.url = mo.group()[20::]