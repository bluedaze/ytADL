import sys
import time
import re
import datetime
import sqlite3

class User_data:
	''' Checks for valid youtube link '''
	def __init__(self):
		self.url = ""
		self.user_link(self.url)

	def __str__(self):
		return "{self.url}".format(self=self)

	def user_link(self, url):
		''' Error message for invalid link. '''
		message = "To create an entry we need the channel url."
		message += "\n\nHere is an example using Google's youtube channel: https://www.youtube.com/channel/UCK8sQmJBp8GCxrOtXWBpyEA" 

		for c in message:
			sys.stdout.write(c)
			sys.stdout.flush()
			time.sleep(.009)
		self.url = input("\n\nPlease provide a similar link: ")
		self.validate_link()

	def validate_link(self):
		''' Validate if this is a url by sending a request to the url. '''
		regex = re.compile(r"(youtube.com/channel/UC)(.{22})")
		mo = regex.search(self.url)

		if mo == None:
			print("~~~~~~~~~~~~~~~\n\n\nThat is not the link we are looking for.\n")
			self.user_link(self.url)
		else:
			self.url = "UU" + mo.group()[22::]

def insert_data(*args):
	insert_Sql = "INSERT INTO yt (channel_title, channel_id, uploads_id, video_id , video_date) VALUES (?, ?, ?, ?, ?)"
	conn = sqlite3.connect('ytadl.db')
	c = conn.cursor()
	try:
		c.execute(insert_Sql, args)
	except sqlite3.IntegrityError:
		pass
	conn.commit()
	c.close()
	conn.close()

def create_db():
	table_sql = "CREATE TABLE IF NOT EXISTS yt (channel_title TEXT, channel_id TEXT, uploads_id TEXT, video_id TEXT NOT NULL UNIQUE, video_date TEXT)"

	conn = sqlite3.connect('ytadl.db')
	c = conn.cursor()
	c.execute(table_sql)
	c.close()
	conn.close()

def query_db():
	# Retrieves video_id matching today's date from the database.
	today = datetime.datetime.now().isoformat()[0:10]
	conn = sqlite3.connect("ytadl.db")
	conn.row_factory = sqlite3.Row
	c = conn.cursor()
	c.execute("SELECT channel_title, channel_id, uploads_id, video_id, video_date FROM yt WHERE video_date = ?;", ( today,))
	selected = [tuple(row) for row in c.fetchall()]
	c.close()
	conn.close()
	return selected

if __name__ == "__main__":
	print(User_data())