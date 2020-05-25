import re
import nltk


def tokens2ngram(tokens, n): 
    '''
    wrapper for nltk ngram generator
    n: n gram specification (assuming n < 6)
    tokens: list of tokenized words 
    '''

    if n == 1: 
        ngrams = tokens 

    else: 

        ngrams = list(nltk.ngrams(tokens, n))
        ngrams = ["_".join(g) for g in ngrams]
    
    return ngrams 


def reddit_preprocess(text): 
    text = re.sub(r'https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n', ' ', text, flags=re.MULTILINE)
    text = re.sub(r'\[removed\]', ' ', text, flags=re.MULTILINE)
    text = re.sub(r'\[deleted\]', ' ', text, flags=re.MULTILINE)
    sentences = nltk.tokenize.sent_tokenize(text)
    sentences = [" ".join(nltk.tokenize.word_tokenize(s)) for s in sentences] 
    return " ".join(sentences) 


def email_preprocess(text): 
    text = re.sub(r'https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n', ' ', text, flags=re.MULTILINE)
    text = re.sub(r'<[\s\S]+>', '', text, flags=re.MULTILINE)
    text = re.sub(r'--', '', text, flags=re.MULTILINE)
    
    sentences = nltk.tokenize.sent_tokenize(text)
    sentences = [" ".join(nltk.tokenize.word_tokenize(s)) for s in sentences] 
    return " ".join(sentences) 
