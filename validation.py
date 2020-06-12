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
		message = "Please provide a link to a youtube channel."
		message += "\n\nHere is an example using Google's youtube channel: https://www.youtube.com/channel/UCK8sQmJBp8GCxrOtXWBpyEA" 

		for c in message:
			sys.stdout.write(c)
			sys.stdout.flush()
			time.sleep(.009)
		self.url = input("\n\nPlease provide a link: ")
		self.validate_link()

	def validate_link(self):
		''' Validate if this is a url by sending a request to the url. '''
		regex = re.compile(r"(youtube.com/channel/UC)(.{22})")
		mo = regex.search(self.url)

		if mo == None:
			self.user_link()
		else:
			self.url = "UU" + mo.group()[22::]


def insert_data(*args):
	insert_Sql = "INSERT INTO yt (channel_title, channel_id, uploads_id, video_id , video_date) VALUES (?, ?, ?, ?, ?)"
	conn = sqlite3.connect('yt.db', isolation_level=None)
	conn.execute('pragma journal_mode=wal;')
	c = conn.cursor()
	c.execute(insert_Sql, args)

def create_db():
	table_sql = "CREATE TABLE IF NOT EXISTS yt (channel_title TEXT, channel_id TEXT, uploads_id TEXT, video_id TEXT, video_date TEXT)"

	conn = sqlite3.connect('yt.db')
	c = conn.cursor()
	c.execute(table_sql)
	c.close()
	conn.close()

def query_db(market):
	#Retrieves video_id matching today's date from the database.
	today = datetime.datetime.now().isoformat()[0:10]
	''' Query database for tweet markets '''
	conn = sqlite3.connect("pidb.db", isolation_level=None)
	conn.row_factory = sqlite3.Row
	c = conn.cursor()
	c.execute("SELECT bracket, buyYes, timeStamp FROM tweets WHERE marketName = ? ORDER BY bracket, timeStamp;", ( market,))
	selected = [tuple(row) for row in c.fetchall()]
	bracketData = {}
	for i in range(9):
		bracket = "B"+str(i+1)
		prices = [(item[1]) for item in selected if item[0] == bracket]
		timeStamp = [(item[2]) for item in selected if item[0] == bracket]
		bracketData[bracket] = prices, timeStamp
	c.close()
	conn.close()
	return bracketData

if __name__ == "__main__":
	print(User_data())