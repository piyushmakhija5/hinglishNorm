#-*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import numpy as np
import pandas as pd
import tqdm
import json
from computeWer import *
from nlgeval import compute_metrics


################## Helper Functions #######################

def getWER(df, candidate, reference):
	annotated_werList = []
	for index, row in tqdm.tqdm(df.iterrows()):
		try:
			annotated_werList.append(wer(row[candidate].strip().split(), row[reference].strip().split()))
		except:
			print(f'error on text: {index, row[candidate]}\n')
	return np.mean(annotated_werList)

def getMetrics(df, candidate, reference):
	with open('ref1.txt','w') as ref:
		for line in list(df.annotation):
			ref.writelines(line+'\n')

	with open('hyp.txt','w') as hyp:
		for line in list(df.normalized):
			hyp.writelines(line+'\n')

	metrics_dict = compute_metrics(hypothesis='hyp.txt', references=['ref1.txt'])
	return metrics_dict
############################ END ###############################


######################## Main Function #########################

if __name__ == "__main__":
    # Read data from command line
    data = sys.argv[1]
    with open(data) as f:
	    json_data = json.load(f)
    df = pd.json_normalize(json_data)
    df = df.reindex(columns=list(json_data[0].keys()))
	# print(df.head())

	# Extract Normalized Dataset's Performance Metrics
    print(getWER(df[:5], 'normalized', 'annotation'))
    print(getMetrics(df[:5], 'normalized', 'annotation'))

###################### END ###############################


