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

def convertLanguage(tags):
    li = []
    for lang in tags:
        if lang == "Hindi":
            li.append("Hindi")
        elif lang != "Unrecognizable or other language":
            li.append("English")
        else:
            li.append("Other")
    return li

def computeCMI(tags):
    twords = len(tags)  # total words in a sentences
    maxWordInAnyLanguage = Counter(tags).most_common(1)[0][1]
    cmi = round(100*(maxWordInAnyLanguage/twords),2)
    return cmi

############################ END ###############################


########## Evaluate text vs annotation Statistics ##############
def getComparisonStats(df):
    statList = []

    # Number of Sentences in Dataset
    statList.append(['#sentences', len(df.inputText), len(df.normalizedText)])

    # Number of Unique Sentences in Dataset
    statList.append(['#uniqueSentences', df.inputText.nunique(), df.normalizedText.nunique()])

    # Number of Unique Words in Dataset
    statList.append(['#uniqueWords', len(set(itertools.chain(*[str.split(x) for x in list(df.inputText)]))),
                    len(set(itertools.chain(*[str.split(x) for x in list(df.normalizedText)])))])

    # Number of Unique Characters in Dataset
    textList = list(df.inputText)
    annotatedList = list(df.normalizedText)
    statList.append(['#uniqueChars', len(set(itertools.chain(*[list(x) for x in textList]))),
                    len(set(itertools.chain(*[list(x) for x in annotatedList])))])

    # Most Common Sentence in Dataset
    statList.append(['mostCommonSentence', str((df.inputText.value_counts().keys()[0])),
                    str(df.normalizedText.value_counts().keys()[0])])

    # Number of Instances for Most Common Sentences in Dataset
    statList.append(['# instances of mostCommonSentence', df.inputText.value_counts().max(),
                    df.normalizedText.value_counts().max()])

    # Mean Character Length of Sentences in Dataset
    statList.append(['meanCharLength', df.inputText.str.len().mean(), df.normalizedText.str.len().mean()])

    # Standard Deviation of Characters for Sentences in Dataset
    statList.append(['stdCharLength', df.inputText.str.len().std(), df.normalizedText.str.len().std()])

    # Median Character Length of Sentences in Dataset
    statList.append(['medianCharLength', df.inputText.str.len().median(),
                    df.normalizedText.str.len().median()])

    # Mean Word Length of Sentences in Dataset
    statList.append(['meanWordLength', df.inputText.str.split().str.len().mean(),
                    df.normalizedText.str.split().str.len().mean()])

    # Standard Deviation of Words for Sentences in Dataset
    statList.append(['stdWordLength', df.inputText.str.split().str.len().std(),
                    df.normalizedText.str.split().str.len().std()])

    # Median Character Length of Sentences in Dataset
    statList.append(['medianWordLength', df.inputText.str.split().str.len().median(),
                    df.normalizedText.str.split().str.len().median()])

    df_stats = pd.DataFrame(data = statList, columns=['feature', 'inputText', 'normalizedText'])
    return df_stats


def getBasicStats(df):
    df.tags = df.tags.apply(ast.literal_eval)
    df['language'] = df.tags.apply(convertLanguage)
    df['cmi'] = df.language.apply(computeCMI)
    print(f"Percentage of sentences where text != annotation: {100.0 * (df.inputText != df.normalizedText).mean():0.2f} %")
    print(f"Percentage of non-English/Hindi Words in Corpus: {df.tags.apply(lambda row: (100.0 * row.count('Unrecognizable or other language')/len(row))).mean():0.2f} %")
    print(f"Percentage of Hindi Words in Corpus: {df.tags.apply(lambda row: (100.0 * row.count('Hindi')/len(row))).mean():0.2f} %")
    print(f"Percentage of sentences containing Hindi-English code-mixing: {100.0 * df.tags.apply(lambda row: 'Hindi' in row).mean():0.2f} %")
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
