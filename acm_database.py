from mysql.connector import MySQLConnection, Error
from dbconfig import read_db_config
import datetime

import MySQLdb
import json

def insertMessages(row):
	query = "INSERT INTO message_status (msg_id,message,processing_status,created_on, error, error_description, callback_url) " \
			"VALUES (%s, %s, %s, %s, %s, %s, %s)"

	f = '%Y-%m-%d %H:%M:%S'
	now = datetime.datetime.now()

	args = (row[0], row[1], row[2], now.strftime(f), row[3], row[4], row[5])

	try:
		db_config = read_db_config()
		conn = MySQLConnection(**db_config)

		cursor = conn.cursor()
		cursor.execute(query, args)

		conn.commit()

	except Error as error:
		print error

	finally:
		cursor.close()
		conn.close()

# def printMessage(uid):
# 	try:
# 		if uid != 0:
# 			db_config = read_db_config()
# 			conn = MySQLConnection(**db_config)
# 			cursor = conn.cursor()

# 			cursor.execute("SELECT id, msg_id, message, callback_url, processing_status FROM message_status WHERE id = "+str(uid))

# 			row = cursor.fetchone()

# 	except Error as error:
# 		print error

# 	finally:
# 		cursor.close()
# 		conn.close()

def fetchPendingJob():
	try:
		db_config = read_db_config()
		conn = MySQLConnection(**db_config)
		cursor = conn.cursor()

		cursor.execute("SELECT id, msg_id, message, callback_url FROM message_status WHERE processing_status=0 ORDER BY id ASC LIMIT 1")

		row = cursor.fetchone()

		if row:
			return int(row[0]), row[1], row[2], row[3]
		return 0, 0, '', ''

	except Error as error:
		print error

	finally:
		cursor.close()
		conn.close()

def updateJobStatus(uid, status):
	query = "UPDATE message_status set processing_status=" + str(status) +" where id="+str(uid)
	try:
		db_config = read_db_config()
		conn = MySQLConnection(**db_config)

		cursor = conn.cursor()

		cursor.execute(query)
		conn.commit()

	except Error as error:
		print error

	finally:
		cursor.close()
		conn.close()

def fileError(uid, error, errorDesc):
	query = "UPDATE message_status set error='1' and errorDesc="+errorDesc+" where id="+str(uid)

	try:
		db_config = read_db_config()
		conn = MySQLConnection(**db_config)

		cursor = conn.cursor()

		cursor.execute(query)
		conn.commit()

	except Error as error:
		print error

	finally:
		cursor.close()
		conn.close()

def updateJobResults(uid, products):
	query = "UPDATE message_status set response_obj = '" + products + "' where id="+str(uid)

	try:
		db_config = read_db_config()
		conn = MySQLConnection(**db_config)

		cursor = conn.cursor()

		cursor.execute(query)
		conn.commit()

	except Error as error:
		print error

	finally:
		cursor.close()
		conn.close()