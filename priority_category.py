import operator

def getMajorityCategory(candidate_values):
	priority = {'Baby': 0.5, 'Beauty': 0.5, 'Car & Motorbike': 0.5, 'Computer & Accessories': 0.75, 
	'Gift Cards': 0.5, 'Grocery & Gourmet Foods': 0.5, 'Health & Personal Care': 0.5, 
	'Home & Kitchen': 0.5, 'Jewellery': 1, 'Industrial & Scientific': 0.5, 'Kindle Store': 1,
	'Movies & TV Shows': 0.5, 'Music' : 0.5, 'Musical Instruments': 1, 'Office Products': 0.5, 
	'Pet Supplies': 0.75, 'Shoes & Handbags' : 1, 'Software': 0.5, 'Video Games': 0.5, 
	'Toys & Games': 0.75, 'Sports, Fitness & Outdoors': 0.5, 'Books': 0.5, 'Electronics': 1.0, 'Music': 0.5, 'Other': 0.25}
	
	category_score = {'Baby': 0.0, 'Beauty': 0.0, 'Car & Motorbike': 0.0, 'Computer & Accessories': 0.0, 
	'Gift Cards': 0.0, 'Grocery & Gourmet Foods': 0.0, 'Health & Personal Care': 0.0, 
	'Home & Kitchen': 0.0, 'Jewellery': 0.0, 'Industrial & Scientific': 0.0, 'Kindle Store': 0.0,
	'Movies & TV Shows': 0.0, 'Music' : 0.0, 'Musical Instruments': 0.0, 'Office Products': 0.0, 
	'Pet Supplies': 0.0, 'Shoes & Handbags' : 0.0, 'Software': 0.0, 'Video Games': 0.0, 
	'Toys & Games': 0.0, 'Sports, Fitness & Outdoors': 0.0, 'Books': 0.0, 'Electronics': 0.0, 'Music': 0.0, 'Other': 0.0}

	for candidate, value in candidate_values.iteritems():
		score = value['score']
		category = value['product_category'].split(';')[0]

		if category not in priority.keys():
			category = "Other"

		category_score[category] += (score * priority[category])

	# print category_score
	return max(category_score.iteritems(), key=operator.itemgetter(1))[0]