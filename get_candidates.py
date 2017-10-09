import nltk
import sys
import re

def getProductCandidates(query):
	allowed_pos = ['NN','CD']

	word_list = nltk.word_tokenize(query)
	pos_list = nltk.pos_tag(word_list)

	# print pos_list
	candidate_list = []
	flag = 0
	candidate = ""

	for item in pos_list:
		word = item[0]
		pos = item[1]
		if(flag == 0 and pos[0:2] == "NN"):
			flag = 1

		if(flag == 1 and pos[0:2] in allowed_pos):
			candidate += word + " "
		elif(flag == 1 and pos[0:2] not in allowed_pos):
			candidate_list.append(candidate[0:len(candidate)-1])
			candidate = ""
			flag = 0

	if(flag == 1):
		candidate_list.append(candidate[0:len(candidate)-1])
	return candidate_list

