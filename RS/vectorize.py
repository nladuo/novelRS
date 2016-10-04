# coding=utf-8
from sklearn import datasets
from sklearn.feature_extraction.text import HashingVectorizer, TfidfTransformer

rawData = datasets.load_files("seg_corpus", encoding="utf-8")
# print rawData.data
vectorizer = HashingVectorizer()
x = vectorizer.transform(rawData.data)
print x
