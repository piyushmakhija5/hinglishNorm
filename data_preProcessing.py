import numpy as np
import pandas as pd
import re
import enchant

# INDIC-TRANSLITERATION
from indic_transliteration import detect
from indic_transliteration import sanscript
from indic_transliteration.detect import Scheme
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate

d = enchant.Dict("en_US")

################## Pre-Process Functions #######################
def regex_or(*items):
    r = '|'.join(items)
    r = '(' + r + ')'
    return r

def pos_lookahead(r):
    return '(?=' + r + ')'

def neg_lookahead(r):
    return '(?!' + r + ')'

def optional(r):
    return '(%s)?' % r

PunctChars = r'''[`'“".?!,:;]'''
Punct = '%s+' % PunctChars
Entity = '&(amp|lt|gt|quot);'

def to_lowerCase(text):
    '''
    Convert text to lower case alphabets
    '''
    return str(text).lower()

def trim(text):
    '''
    Trim leading and trailing spaces in the text
    '''
    return text.strip().strip('.')

def strip_whiteSpaces(text):
    '''
    Strip all white spaces
    '''
    text = re.sub(r'[\s]+', ' ', text)
    return text

def process_URLs(text):
    '''
    Replace all URLs in the  text
    '''
    UrlStart1 = regex_or('https?://', r'www\.')
    CommonTLDs = regex_or('com','co\\.uk','org','net','info','ca','biz','info','edu','in','au')
    UrlStart2 = r'[a-z0-9\.-]+?' + r'\.' + CommonTLDs + pos_lookahead(r'[/ \W\b]')
    UrlBody = r'[^ \t\r\n<>]*?'  # * not + for case of:  "go to bla.com." -- don't want period
    UrlExtraCrapBeforeEnd = '%s+?' % regex_or(PunctChars, Entity)
    UrlEnd = regex_or( r'\.\.+', r'[<>]', r'\s', '$')
    Url =   (optional(r'\b') +
            regex_or(UrlStart1, UrlStart2) +
            UrlBody +
    pos_lookahead( optional(UrlExtraCrapBeforeEnd) + UrlEnd))

    Url_RE = re.compile("(%s)" % Url, re.U|re.I)
    text = re.sub(Url_RE, ' ', text)

    # fix to handle unicodes in URL
    URL_regex2 = r'\b(htt)[p\:\/]*([\\x\\u][a-z0-9]*)*'
    text = re.sub(URL_regex2, ' ', text)
    return text

def apply_transliteration(text):
    '''
    Detect Language and Transliterate non-Roman script text into Roman script
    '''
    lang = detect.detect(str(text))
    if lang not in [Scheme.ITRANS, Scheme.HK, Scheme.SLP1, Scheme.IAST, Scheme.Velthuis, Scheme.Kolkata]:
        text = transliterate(text, getattr(sanscript, lang.upper()), sanscript.HK).lower()
    return text

def filter_alpha_numeric(text):
    '''
    Filter out words which have non-Alpha-numeric characters
    '''
    if text!=None:
        tokens = text.split()
        clean_tokens = [t for t in tokens if re.match(r'[^\W\d_\']*$', t)]
        return ' '.join(clean_tokens)
    else:
        return text

def normalize_word(text):
    if text!=None:
        text = re.sub(r'(.)\1+', r'\1\1', text)
        return text
    else:
        return text

def remove_non_ascii(text):
    if text!=None:
        return ''.join(i for i in text if ord(i)<128)
    else:
        return text

def remove_empty(df):
    df['text'].replace('', np.nan, inplace=True)
    df['text'].replace(r'^\s*$', np.nan, inplace=True)
    df.dropna(subset=['text'], inplace=True)
    return df

################################# END ###################################

################## Driver Function #########################

def preprocess(df):
    if 'text' not in df.columns:
        raise ValueError("text column not present in excel")
    print("Processing ..")
    print("Total length : -",len(df))
    df['text'] = df['text'].apply(apply_transliteration)
    df['text'] = df['text'].apply(to_lowerCase)
    df['text'] = df['text'].apply(process_URLs)
    df['text'] = df['text'].apply(filter_alpha_numeric)
    df['text'] = df['text'].apply(remove_non_ascii)
    df['text'] = df['text'].apply(normalize_word)
    df['text'] = df['text'].apply(trim)
    df['text'] = df['text'].apply(strip_whiteSpaces)
    df = remove_empty(df)
    df = df.reset_index(drop=True)
    return df

###################### END ###############################

################## Main Function #########################

if __name__ == "__main__":
    df  = pd.read_excel('rawTextUtterances.xlsx')
    df = preprocess(df)
    df.to_excel("preprocessedUtterances.xlsx", index=False)
###################### END ###############################
