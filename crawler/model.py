# coding=utf-8


class Novel:
    def __init__(self, name, author, category, word_num, url, is_crawled, success):
        self.name = name
        self.author = author
        self.category = category
        self.word_num = word_num
        self.url = url
        self.is_crawled = is_crawled    # 是否爬取过章节
        self.success = success          # 爬取章节是否成功

    def dict(self):
        return {
            'name': self.name,
            'author': self.author,
            'category': self.category,
            'word_num': self.word_num,
            'url': self.url,
            'is_crawled': self.is_crawled,
            'success': self.success
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
