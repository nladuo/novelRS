# coding=utf-8


class Novel:
    """ 小说结构 """
<<<<<<< HEAD
    def __init__(self, name, url, author, category, abstract, download_url):
=======
    def __init__(self, name, author, category, status, url):
>>>>>>> d1c89e5fe74cc909059c045815cf1f23cea14dba
        self.name = name
        self.url = url
        self.author = author
        self.category = category
<<<<<<< HEAD
        self.abstract = abstract
        self.download_url = download_url
=======
        self.status = status
        self.url = url
>>>>>>> d1c89e5fe74cc909059c045815cf1f23cea14dba

    def dict(self):
        return {
            'name': self.name,
            'url': self.url,
            'author': self.author,
            'category': self.category,
<<<<<<< HEAD
            'abstract': self.abstract,
            'download_url': self.download_url,
            'is_downloaded': False,                 # 是否下载
            'success': True,                        # 下载是否成功
=======
            'status': self.status,
            'url': self.url,
            'is_crawled': False,                # 是否爬取过章节
            'success': True,                    # 爬取章节是否成功(即是否超过300章)
            'is_segment': False,                # 有没有分割过
            'is_compute': False,                # 有没有计算过相似度
            'similarities': ""                  # 记录相似的小说
        }


class Chapter:
    """ 储存小说章节 """
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
>>>>>>> d1c89e5fe74cc909059c045815cf1f23cea14dba
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
