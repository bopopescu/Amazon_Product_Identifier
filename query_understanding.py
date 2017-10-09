import nltk
import sys
import re

from get_candidates import getProductCandidates
from search import getTitle
from product_category import getProductCategory
from score_calculator import calculateRelevancy
from priority_category import getMajorityCategory

# query = "We are the sole providers of apple and Samsung Galaxy phones in Hyderabad"

def extractProducts(query):
	candidate_values = {}

	candidates = getProductCandidates(query)
	# print "Extracted Candidates"
	# print candidates

	for candidate in candidates:
		# print 
		# print "Candidate = " + candidate
		
		attr = {'title': '', 'product_category': '', 'score': 0.0}

		delimeter = "+"
		tokens = candidate.split()

		for index in range(0, len(tokens)):
			word = delimeter.join(tokens[index:len(tokens)])
			# print "Word = " + word
			page = "http://www.amazon.in/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords="+word
			
			# print page
			# Returns the title of the first product matched.
			# print word, page
			title = getTitle(page)
			if title:
				# print title
				product_name = title[0]
				product_page = title[1]
				
				product_category = getProductCategory(product_page)

				if product_category:
					# print "Category = " + product_category
					candidate_values[candidate] = attr
					candidate_values[candidate]['title'] = product_name

					candidate_values[candidate]['product_category'] = product_category
					
					score = calculateRelevancy(candidate,product_name)
					candidate_values[candidate]['score'] = score
					# print product_name, product_category

					break


	majority_category = getMajorityCategory(candidate_values)
	# print "Majority Category = " + majority_category

	products_list = {}

	for key, value in candidate_values.iteritems():
		# print "Key = " + key
		category = value['product_category'].split(';')[0]

		if(category == majority_category):
			products_list[key] = value

	return products_list, 0, ''