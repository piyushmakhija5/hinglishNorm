#-*- coding: utf-8 -*-
#!/usr/bin/env python


# Script adapted from here https://github.com/zszyellow/WER-in-python
import sys
import numpy as np
import pandas as pd
import tqdm
from nltk.translate.bleu_score import sentence_bleu, corpus_bleu


def sentenceBleu(ref, can):
	reference = pd.read_table(ref,header=None)
	candidate = pd.read_table(can,header=None)

	if len(reference) != len(candidate):
		raise ValueError('The number of sentences in both files do not match.')

	df = pd.DataFrame()
	df['ref'] = pd.Series(reference[0]).astype(str) + '\n'
	df['can'] = pd.Series(candidate[0]).astype(str) + '\n'
	
	#print (df.tail())
	score = 0.
	#print (sentence_bleu([["bahar", "hun", "abi", "ok"]], ["baahar", "hun", "abhi", "okay"]))
	for i in tqdm.tqdm(range(len(reference))):
		a = [df['ref'][i].split()]
		b = df['can'][i].split()
		#print (a,b)
		n = min(4, len(a[0]), len(b))
		w = tuple([1. / n] * n)
		score += sentence_bleu(a, b, weights= w)
		#print (score, a, b)
	score /= len(reference)
	print("The average sentence level bleu score is: "+str(score))


def weightedBleu(ref, can, w = [0.4, 0.3, 0.2, 0.1]):
	reference = open(ref, 'r').readlines()
	candidate = open(can, 'r').readlines()
	if len(reference) != len(candidate):
		raise ValueError('The number of sentences in both files do not match.')

	score = 0.
	for i in tqdm.tqdm(range(len(reference))):
		a= [reference[i].strip().split()]
		b= candidate[i].strip().split()
		n = min(4, len(a[0]), len(b))
		w1 = np.divide(w[:n],[sum(w[:n])]*n)
		#print(w1, [sum(w[:n])]*n, a, b)
		score += sentence_bleu(a, b, weights = w1)
	score /= len(reference)
	print("The average weighted sentence level bleu score is: "+str(score))


def corpusBleu(ref, can):
	reference = open(ref, 'r').readlines()
	candidate = open(can, 'r').readlines()

	score = corpus_bleu([reference.split()], candidate.split())
	print("The average sentence level bleu score is: "+str(score))


if __name__ == '__main__':
    ref = sys.argv[1]
    can = sys.argv[2]
    sentenceBleu(ref, can)
    weightedBleu(ref, can)
    weightedBleu(ref, can, w=[1.0, 0.0, 0.0, 0.0])
