"""
语料处理相关常用函数
"""
import pathlib

import nltk

STOPWORDS_NLTK = {'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves',
                  'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves',
                  'he', 'him', 'his', 'himself',
                  'she', "she's", 'her', 'hers', 'herself',
                  'it', "it's", 'its', 'itself',
                  'they', 'them', 'their', 'theirs', 'themselves',
                  'what', 'which', 'who', 'whom',
                  'this', 'that', "that'll", 'these', 'those',
                  'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                  'have', 'has', 'had', 'having',
                  'do', 'does', 'did', 'doing',
                  'a', 'an', 'the',
                  'and', 'but', 'if', 'or', 'because', 'as', 'until',
                  'while', 'of', 'at', 'by', 'for', 'with',
                  'about', 'against', 'between', 'into', 'through', 'during', 'before',
                  'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in',
                  'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
                  'here', 'there',
                  'when', 'where', 'why', 'how',
                  'all', 'any', 'both', 'each',
                  'few', 'more', 'most', 'other', 'some', 'such',
                  'no', 'nor', 'not', 'only', 'own', 'same',
                  'so', 'than', 'too', 'very',
                  's', 't',
                  'can', 'will', 'just',
                  'don', "don't", 'should', "should've",
                  'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain',
                  'aren', "aren't",
                  'couldn', "couldn't",
                  'didn', "didn't", 'doesn', "doesn't",
                  'hadn', "hadn't", 'hasn',
                  "hasn't", 'haven', "haven't",
                  'isn', "isn't", 'ma',
                  'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't",
                  'shan', "shan't", 'shouldn', "shouldn't",
                  'wasn', "wasn't", 'weren', "weren't",
                  'won', "won't", 'wouldn', "wouldn't"}


def remove_stopwords(words, stopwords=None, encoding=None):
    """
    去除停用词

    默认处理英文，且使用 nltk 定义的停用词

    Args:
        words(list of str): 待处理的文本，可以是已分词的字符串或词列表
        stopwords(list or file):

    Returns:

    """
    if stopwords is None:
        stopwords = STOPWORDS_NLTK
    elif pathlib.Path(stopwords).is_file():
        with open(stopwords, encoding=encoding) as f:
            stopwords = set(word.strip() for word in f)
    else:
        stopwords = set(stopwords)

    return [w for w in words if w not in stopwords]
