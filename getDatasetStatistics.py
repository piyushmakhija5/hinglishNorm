# Code file to extract Dataset Statistics

import numpy as np
import pandas as pd
import itertools
import sys
import ast
from collections import Counter
import json

pd.options.display.float_format = "{:,.2f}".format

################## Helper Functions #######################

def convertLanguage(transformation):
    li = []
    for lang in transformation:
        if lang != "Hindi":
            li.append("English")
        else:
            li.append(lang)
    return li

def computeCMI(transformation):
    twords = len(transformation)  # total words in a sentences
    maxWordInAnyLanguage = Counter(transformation).most_common(1)[0][1]
    cmi = round(100*(maxWordInAnyLanguage/twords),2)
    return cmi

############################ END ###############################


########## Evaluate text vs annotation Statistics ##############
def getComparisonStats(df):
    statList = []

    # Number of Sentences in Dataset
    statList.append(['#sentences', len(df.text), len(df.annotation)])

    # Number of Unique Sentences in Dataset
    statList.append(['#uniqueSentences', df.text.nunique(), df.annotation.nunique()])

    # Number of Unique Words in Dataset
    statList.append(['#uniqueWords', len(set(itertools.chain(*[str.split(x) for x in list(df.text)]))),
                    len(set(itertools.chain(*[str.split(x) for x in list(df.annotation)])))])

    # Number of Unique Characters in Dataset
    textList = list(df.text)
    annotatedList = list(df.annotation)
    statList.append(['#uniqueChars', len(set(itertools.chain(*[list(x) for x in textList]))),
                    len(set(itertools.chain(*[list(x) for x in annotatedList])))])

    # Most Common Sentence in Dataset
    statList.append(['mostCommonSentence', str((df.text.value_counts().keys()[0])),
                    str(df.annotation.value_counts().keys()[0])])

    # Number of Instances for Most Common Sentences in Dataset
    statList.append(['# instances of mostCommonSentence', df.text.value_counts().max(),
                    df.annotation.value_counts().max()])

    # Mean Character Length of Sentences in Dataset
    statList.append(['meanCharLength', df.text.str.len().mean(), df.annotation.str.len().mean()])

    # Standard Deviation of Characters for Sentences in Dataset
    statList.append(['stdCharLength', df.text.str.len().std(), df.annotation.str.len().std()])

    # Median Character Length of Sentences in Dataset
    statList.append(['medianCharLength', df.text.str.len().median(),
                    df.annotation.str.len().median()])

    # Mean Word Length of Sentences in Dataset
    statList.append(['meanWordLength', df.text.str.split().str.len().mean(),
                    df.annotation.str.split().str.len().mean()])

    # Standard Deviation of Words for Sentences in Dataset
    statList.append(['stdWordLength', df.text.str.split().str.len().std(),
                    df.annotation.str.split().str.len().std()])

    # Median Character Length of Sentences in Dataset
    statList.append(['medianWordLength', df.text.str.split().str.len().median(),
                    df.annotation.str.split().str.len().median()])

    df_stats = pd.DataFrame(data = statList, columns=['feature', 'text', 'annotation'])
    return df_stats


def getBasicStats(df):
    df.transformation = df.transformation.apply(ast.literal_eval)
    df['language'] = df.transformation.apply(convertLanguage)
    df['cmi'] = df.transformation.apply(computeCMI)
    print(f"Percentage of sentences where text != annotation: {100.0 * (df.text != df.annotation).mean():0.2f} %")
    print(f"Percentage of sentences with Hindi Words: {100.0 * df.transformation.apply(lambda row: 'Hindi' in row).mean():0.2f} %")
    print(f"Percentage of Hindi Words in Corpus: {df.transformation.apply(lambda row: (100.0 * row.count('Hindi')/len(row))).mean():0.2f} %")
    print(f"Average CMI : {df.cmi.mean():0.2f}")


####################################### END ########################################


############################## Driver Function #####################################

if __name__ == "__main__":
    # Read data from command line
    data = sys.argv[1]
    with open(data) as f:
	    json_data = json.load(f)
    df = pd.json_normalize(json_data)
    df = df.reindex(columns=list(json_data[0].keys()))

    # Evaluate Dataset statistics
    df_stats = getComparisonStats(df)

    #Print Results
    getBasicStats(df)
    print(df_stats)

####################################### END #########################################
