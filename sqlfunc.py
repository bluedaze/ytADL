import sys
import sqlite3
from rich.console import Console
from rich.table import Column, Table

class Information:
	def __init__(self):
		self.create_db()
		self.data = self.query_db()


	def create_db(self):
	    conn = sqlite3.connect("ytadl.db")
	    c = conn.cursor()
	    c.execute(
	        "CREATE TABLE IF NOT EXISTS ytadl (channel_title TEXT, channel_id TEXT, uploads_id TEXT, video_id TEXT NOT NULL UNIQUE, video_date TEXT, video_title TEXT, description TEXT, downloaded TEXT)"
	    )
	    c.close()
	    conn.close()


	def query_db(self):
		conn = sqlite3.connect("ytadl.db")
		conn.row_factory = sqlite3.Row
		c = conn.cursor()
		c.execute(
		"SELECT * FROM ytadl;"
		)
		selected = [tuple(row) for row in c.fetchall()]
		c.close()
		conn.close()
		return selected

	def insert_data(self, *args):
	    insert_Sql = "INSERT INTO ytadl (channel_title, channel_id, uploads_id, video_id, video_date, video_title, description, downloaded) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
	    conn = sqlite3.connect("ytadl.db")
	    c = conn.cursor()
	    try:
	        c.execute(insert_Sql, args)
	    except sqlite3.IntegrityError:
	        pass
	    conn.commit()
	    c.close()
	    conn.close()

	def mark_downloaded(self, video_id):
	    conn = sqlite3.connect("ytadl.db")
	    c = conn.cursor()
	    c.execute("UPDATE ytadl SET 'downloaded' = 1 WHERE video_id = ?", (video_id,))
	    conn.commit()
	    c.close()
	    conn.close()

	def channels(self):
		channel_set = set()
		for i in self.data:
			channel_set.add(i[0])
			display_string = ""
		return channel_set

	def videos(self):
		videos_list = []
		for i in self.data:
			channel_title = i[0]
			video_title = i[5]
			videos_list.append(f"{channel_title} - {video_title}")
		return videos_list

	def display(self, iterable, heading = None):
		display_string = ""
		if heading is None:
			heading = "Information"
		for i in iterable:
			display_string += i + "\n"
		console = Console()
		table = Table(show_header=True, header_style="bold red3")
		table.add_column(f"{heading}", style="dim", width=96)
		table.add_row(f"[#5fffff]{display_string}")
		console.print(table)
		return display_string

	def in_queue(self):
		queue_dict = []
		for i in self.data:
			downloaded = i[7]
			if downloaded == "0":
				channel_title = i[0]
				channel_id = i[1]
				uploads_id = i[2]
				video_id = i[3]
				video_date = i[4]
				video_title = i[5]
				description = i[6]
				downloaded = i[7]
				d = {"channel_title": channel_title,
				"channel_id": channel_id,
				"uploads_id": uploads_id,
				"video_id": video_id,
				"video_date": video_date,
				"video_title": video_title,
				"description": description,
				"downloaded": downloaded}
				queue_dict.append(d)
		return queue_dict



if __name__ == "__main__":
	obj = Information()
	data = obj.query_db()
	for i in data:
		print(i[1])
# videos = User_data().videos()
# display = User_data().display(videos)