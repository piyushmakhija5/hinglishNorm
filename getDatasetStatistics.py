# Code file to extract Dataset Statistics

import numpy as np
import pandas as pd
import itertools
pd.options.display.float_format = "{:,.2f}".format

df = pd.read_csv('10kAnnotations_processed.csv')


############################## Evaluate Statistics #################################
statList = []

# Number of Utterances in Dataset
statList.append(['#Utterances', len(df.processedUtterance), len(df.processedAnnotation)])

# Number of Unique Utterances in Dataset
statList.append(['#uniqueUtterances', df.processedUtterance.nunique(), df.processedAnnotation.nunique()])

# Number of Unique Words in Dataset
statList.append(['#uniqueWords', len(set(itertools.chain(*[str.split(x) for x in list(df.processedUtterance)]))), 
                len(set(itertools.chain(*[str.split(x) for x in list(df.processedAnnotation)])))])

# Number of Unique Characters in Dataset
utteranceList = list(df.processedUtterance)
annotatedList = list(df.processedAnnotation)
statList.append(['#uniqueChars', len(set(itertools.chain(*[list(x) for x in utteranceList]))), 
                len(set(itertools.chain(*[list(x) for x in annotatedList])))])

# Most Common Utterance in Dataset
statList.append(['mostCommonUtterance', df.processedUtterance.value_counts().argmax(), 
                 df.processedAnnotation.value_counts().argmax()])

# Number of Instances for Most Common Utterances in Dataset
statList.append(['# instances of mostCommonUtterance', df.processedUtterance.value_counts().max(), 
                 df.processedAnnotation.value_counts().max()])

# Mean Character Length of Utterances in Dataset
statList.append(['meanCharLength', df.processedUtterance.str.len().mean(), df.processedAnnotation.str.len().mean()])

# Standard Deviation of Characters for Utterances in Dataset
statList.append(['stdCharLength', df.processedUtterance.str.len().std(), df.processedAnnotation.str.len().std()])

# Median Character Length of Utterances in Dataset
statList.append(['medianCharLength', df.processedUtterance.str.len().median(),
                 df.processedAnnotation.str.len().median()])

# Mean Word Length of Utterances in Dataset
statList.append(['meanWordLength', df.processedUtterance.str.split().str.len().mean(), 
                 df.processedAnnotation.str.split().str.len().mean()])

# Standard Deviation of Words for Utterances in Dataset
statList.append(['stdWordLength', df.processedUtterance.str.split().str.len().std(), 
                 df.processedAnnotation.str.split().str.len().std()])

# Median Character Length of Utterances in Dataset
statList.append(['medianWordLength', df.processedUtterance.str.split().str.len().median(), 
                 df.processedAnnotation.str.split().str.len().median()])

####################################### END ########################################


############################## Driver Function #####################################

# Create Dataset for Datset Statistics
df_stats = pd.DataFrame(data = statList, columns=['feature', 'noisy_utterance', 'annotated_utterance'])
print(df_stats)

####################################### END #########################################
