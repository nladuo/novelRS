# coding=utf-8


class Novel:
    """ 小说结构 """
    def __init__(self, name, url, author, category, abstract, download_url):
        self.name = name
        self.url = url
        self.author = author
        self.category = category
        self.abstract = abstract
        self.download_url = download_url

    def dict(self):
        return {
            'name': self.name,
            'url': self.url,
            'author': self.author,
            'category': self.category,
            'abstract': self.abstract,
            'download_url': self.download_url,
            'is_downloaded': False,                 # 是否下载
            'success': True,                        # 下载是否成功,
            'is_segment': False,                    # 是否分词
        }


class FailedUrl:
    """ 失败的链接 """
    def __init__(self, url):
        self.url = url

    def dict(self):
        return {'url': self.url}


class Similarity:
    """ 保存两个小说之间相似度 """
    def __init__(self, novel_id, similarity):
        self.novel_id = novel_id
        self.similarity = similarity

    def dict(self):
        return {
            'novel_id': self.novel_id,
            'similarity': self.similarity,
        }
