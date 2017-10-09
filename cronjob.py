from acm_database import insertMessages, updateJobStatus, fetchPendingJob, updateJobResults
from connect import connect

from query_understanding import *

import json
import requests

# Triggered by two events
# 1. New request comes to the engine
# 2. Processing of request by the system is done, so the thread is free.

############# PROCESSING STATUS ################################
# 0: Job is Pending 
# 2: Job is under processing
# 1: Job successfully completed, results stored in database
# -1: Job failed with error
# 3: Callback successful
################################################################

TOTAL_THREADS = 2
used_threads = 0

print "\nTOTAL THREADS = " + str(TOTAL_THREADS) + "\n"

def acquireThread():
	global used_threads
	used_threads += 1
	
def releaseThread():
	global used_threads
	used_threads -= 1

def runProductExtractor(query):
	products, error, errorDesc = extractProducts(query);
	return products, error, errorDesc

def getNewJob():
	global used_threads, TOTAL_THREADS
	uid, msg_id, query, callback_url = fetchPendingJob()
	
	if uid:
		updateJobStatus(uid, 2)

		acquireThread()
		return uid, msg_id, query, callback_url
	else:
		return 0, 0, '', ''

def recallProcess():
	runProcess()

def runProcess():
	global used_threads, TOTAL_THREADS

	print "Threads left = " + str(TOTAL_THREADS - used_threads)

	if(used_threads < TOTAL_THREADS):
		uid, msg_id, query, callback_url = getNewJob()

		if uid:
			print "Thread acquired ..."
			print "New Job assigned with ID = " + str(uid)
			products, error, errorDesc = runProductExtractor(query)
			
			if error:
				print "Encountered error while processing"
				updateJobStatus(uid, -1)
				fileError(uid, error, errorDesc)
			else:
				print "Successfully completed the job with results"
				print products
				updateJobStatus(uid, 1)
				updateJobResults(uid, json.dumps(products))
				
				# print type(uid)
				response = {}
				response['uid'] = str(msg_id)
				response['products'] = []
				
				count = 0
				for key, value in products.iteritems():
					response['products'].append({})

					# query_word, product_name, category, score, description, imageuri, price, externalSourceName
					response['products'][count]['queryProductName'] = key
					response['products'][count]['productCategory'] = value['product_category']
					response['products'][count]['queryProductScore'] = str(value['score'])
					response['products'][count]['productName'] = value['title']

					response['products'][count]['productDescription'] = ''
					response['products'][count]['imageUri'] = []
					response['products'][count]['price'] = 0.0
					response['products'][count]['externalSourceName'] = ''

					count += 1

				print json.dumps(response)
				headers = {'content-type' : 'application/json'}
				r = requests.post(callback_url, data = json.dumps(response), headers=headers)
				# print r.text
				

			releaseThread()
			print "Thread released ..."

			recallProcess()

		# 	# callback_return 
		# 	# Update callback status

		else:
			print "No new Job"
	else:
		print "===== All threads occupied ======"
