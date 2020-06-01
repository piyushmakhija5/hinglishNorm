#-*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import numpy as np
import pandas as pd
import tqdm
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


with open('ref1.txt','w') as ref:
    for line in list(df.annotation):
        ref.writelines(line+'\n')
        
with open('hyp.txt','w') as hyp:
    for line in list(df.normalized):
        hyp.writelines(line+'\n')
        
metrics_dict = compute_metrics(hypothesis='hyp.txt', references=['ref1.txt'])
############################ END ###############################


######################## Main Function #########################

if __name__ == "__main__":
    # Read data from command line
    data = sys.argv[1]
    df  = pd.read_json(data)
	# print(df.head())
    
	# Preprocess Dataset
    print(getWER(df[:5], 'normalized', 'annotation'))
	print(metrics_dict)

###################### END ###############################


