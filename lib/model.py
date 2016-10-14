# coding=utf-8


class Novel:
    def __init__(self, name, author, category, word_num, url):
        self.name = name
        self.author = author
        self.category = category
        self.word_num = word_num
        self.url = url

    def dict(self):
        return {
            'name': self.name,
            'author': self.author,
            'category': self.category,
            'word_num': self.word_num,
            'url': self.url,
            'is_crawled': False,                # 是否爬取过章节
            'success': True,                    # 爬取章节是否成功
            'is_segment': False,                # 有没有分割过
            'is_vectorize': False,              # 有没有向量化
            'vector': '[]',                     # 向量化
            'tfidf_vector': '[]',               # tf-idf向量化
            'is_compute': False,                # 有没有计算过相似度
            'cluster': -1,                      # 聚类的类别
            'similarities': ""                  # 记录相似的小说
        }


class Chapter:
    def __init__(self, novel_id, name, url, content=''):
        self.novel_id = novel_id
        self.name = name
        self.url = url
        self.content = content

    def dict(self):
        return {
            'novel_id': self.novel_id,
            'name': self.name,
            'url': self.url,
            'content': self.content
        }


class FailedUrl:

    def __init__(self, url):
        self.url = url

    def dict(self):
        return {'url': self.url}


class Similarity:
    """ 保存两个小说之间相似度 """
    def __init__(self, _id, similarity):
        self._id = _id
        self.similarity = similarity

    def dict(self):
        return {
            '_id': self._id,
            'similarity': self.similarity,
        }
