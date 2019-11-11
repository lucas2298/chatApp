import numpy as np
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()


def clean_up_sentence(sentence):
	#Tokenize sentence
	sentence_words = nltk.word_tokenize(sentence)
	#lowercase each word
	sentence_words = [word.lower() for word in sentence_words]
	return sentence_words

def bow(sentence, words):
	#Tokenize the pattern
	sentence_words = clean_up_sentence(sentence)
	#Bag of words
	bag = [0]*len(words)
	for s in sentence_words:
		for i, w in enumerate(words):
			if s == w:
				bag[i] = 1
	return(np.array(bag))