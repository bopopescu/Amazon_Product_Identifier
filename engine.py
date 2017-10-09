from flask import Flask
from flask import request
from flask import jsonify
from flask import Response
import json
import unicodedata

from query_understanding import *
from acm_database import insertMessages
from cronjob import *

app = Flask(__name__)

@app.route("/getProduct", methods=['POST'])
def getProduct():
	data = request.get_json()

	uid = unicodedata.normalize('NFKD', data['uid']).encode('ascii','ignore')
	query = unicodedata.normalize('NFKD', data['query']).encode('ascii','ignore')
	callback_url = unicodedata.normalize('NFKD', data['callback_url']).encode('ascii','ignore')

	insertMessages([uid, query, 0, 0, '', callback_url])
	runProcess()

	return "1"

@app.route("/ping", methods=['GET'])
def ping():
	return "1"

if __name__ == "__main__":
	app.run(host='0.0.0.0',port=5000,debug=True,threaded=True)

