# coding=utf-8
from gensim import corpora


# print "你好 小明".split()
dictionary = corpora.Dictionary(["你好 小明 小李".split()])

# dictionary.add_documents([["小李"]])

print dictionary.doc2bow("你好 你好 小明 小李 111".split(" "))
#
#
print dictionary.token2id
#
# print dictionary
#
