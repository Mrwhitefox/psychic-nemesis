# -*- coding: utf-8 -*-
import sqlite3
import sys
import os
class Mursqlite(object):

	def __init__(self, dbPath):
		if not os.path.isfile(dbPath):
			print("File not found.")
			return None
		self.dbPath = dbPath
		self.cnx = None

	def query(self, req):

		try:
			con = sqlite3.connect(self.dbPath)
			cur = con.cursor()
			cur.execute(req)
			res = cur.fetchall()
			return res

		except sqlite3.Error as e:
			print ("Exception:")
			print(e.args)
		finally:
			con.close()
