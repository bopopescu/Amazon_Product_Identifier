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

	uid = int(unicodedata.normalize('NFKD', data['uid']).encode('ascii','ignore'))
	query = unicodedata.normalize('NFKD', data['query']).encode('ascii','ignore')
	callback_url = unicodedata.normalize('NFKD', data['callback_url']).encode('ascii','ignore')

	# products = extractProducts(query);
	# return json.dumps(products)
	
	insertMessages([uid, query, 0, 0, '', callback_url])
	runProcess()
	return "Done"



if __name__ == "__main__":
	app.run(host='127.0.0.1',port=5001,debug=True,threaded=True)

