import nltk
import sys
import re

from nltk.tokenize import RegexpTokenizer
from nltk.stem.lancaster import LancasterStemmer

st = LancasterStemmer()

allowed_pos = ['NN','CD','JJ']

def preprocess(words):
	new_words = []
	for word in words:
		new_words.append(st.stem(word.lower()))
	return new_words

def getLastNoun(pos_list):
	final_word = ""
	for item in pos_list:
		word = item[0]
		pos = item[1]

		if(pos[0:2] == "NN"):
			final_word = word

	return word

def feature1_score(candidate_words,title_words):
	num_words = len(candidate_words)
	count = 1
	score = 0
	for i in range(num_words-1,-1,-1):
		if(candidate_words[i] in title_words):
			score += (1.0/count)
		count+=1
	
	return score

def feature2_score(candidate_words,title_words):
	last_noun_word = getLastNoun(nltk.pos_tag(candidate_words))

	pos_list = nltk.pos_tag(title_words)
	num_words = len(pos_list)
	count = 1
	score = 0
	
	for i in range(num_words-1,-1,-1):
		item = pos_list[i]
		word = item[0]
		pos = item[1]
		if(pos not in allowed_pos):
			count = 1

		if(word == last_noun_word):
			score += (1.0/count)

		count+=1
	return score

def check_NNP(candidate):
	word_list = nltk.word_tokenize(candidate)
	pos_list = nltk.pos_tag(word_list)

	# print pos_list
	# print "Candidate = " + candidate
	flag = 0
	for item in pos_list:
		if(item[1] == "NNP"):
			return 1
	return 0

def calculateRelevancy(candidate,title):
	candidate_words = preprocess(nltk.word_tokenize(candidate))
	# print candidate_words
	
	tokenizer = RegexpTokenizer(r'\w+')
	title_words = preprocess(tokenizer.tokenize(title))
	# print title_words

	f1_score = feature1_score(candidate_words,title_words)
	f2_score = feature2_score(candidate_words,title_words)

	NNP_score = check_NNP(candidate)

	score = f1_score + 2*f2_score

	if(NNP_score == 1):
		score *= 2

	return score