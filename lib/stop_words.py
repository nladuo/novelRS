# coding=utf-8

import os

def load_stop_words():
    """ 停用词来自: http://blog.csdn.net/shijiebei2009/article/details/39696571 """
    words = []
    txt_path = os.path.join("..", "lib", "stop_words.txt")
    with open(txt_path, "rb") as f:
        for line in f.readlines():
            words.append(line.strip(" "))
            # print "--%s--" % line.strip(" ").strip("\n")
    return words


stop_words = load_stop_words()
