# coding=utf-8
from gevent import monkey; monkey.patch_all()
import gevent
from gevent import queue
from model import *
from utils import *
from config import *
from bs4 import BeautifulSoup
import sys
import time


reload(sys)
sys.setdefaultencoding('utf8')


class ChapterCrawler:

    def __init__(self):
        self.client = init_client()
        self.db = self.client[config['db_name']]
        self.novels = self.db.novels.find({'is_crawled': False})
        self.collection = self.db.chapters
        self.collection.ensure_index('url', unique=True)

    def run(self):
        novels = []
        for novel in self.novels:
            n = Novel(
                novel['name'],
                novel['author'],
                novel['category'],
                novel['word_num'],
                novel['url'],
                False,
                True
            )
            n._id = novel['_id']
            novels.append(n)

        for novel in novels:
            print novel._id, "  ---> scraping", novel.name, novel.author, time.strftime("%Y-%m-%d %H:%M:%S",
                                                                      time.localtime(time.time()))
            html = get_body(novel.url)
            pre_chapters = self.__parse_chapters(novel._id, novel.url, html)
            pre_chapters_set = self.__split_pre_chapters(pre_chapters)
            chapter_count = 0
            for pre_chapters in pre_chapters_set:
                tasks = []
                q = gevent.queue.Queue()

                for chapter in pre_chapters:
                    tasks.append(gevent.spawn(self.__async_get_chapter_content, chapter, q))
                gevent.joinall(tasks)

                while not q.empty():
                    dict = q.get()
                    body = dict['body']
                    chapter = dict['chapter']
                    if len(body) == 0:
                        add_failed_url(self.db, chapter.url)
                        continue
                    print "success --->", chapter.url
                    try:
                        content = self.__parse_chapter_content(body)
                        chapter.content = content
                        self.__add_chapter(chapter)
                        chapter_count += 1
                        # 硬盘空间不够，每本小说最多只爬取100章
                        if chapter_count >= 100:
                            break
                    except: pass
            # 小于100章的小说不进行统计，把novel的success设为0
            if chapter_count < 100:
                self.__update_failed_novel(novel)
            self.__update_novel(novel)  # 把novel的is_crawled设为1

        self.__close()

    def __split_pre_chapters(self, pre_chapters, num=50):
        return [pre_chapters[i: i + num] for i in range(len(pre_chapters)) if i % num == 0]

    def __async_get_chapter_content(self, chapter, q):
        body = get_body(chapter.url)
        q.put({'chapter': chapter, 'body': body})
        print chapter.url

    def __parse_chapters(self, _id, url, html):
        chapters = []
        bs_obj = BeautifulSoup(html)
        tds = bs_obj.find_all('td', {'class', 'L'})
        for td in tds:
            if td.text.strip() != '':
                chapters.append(Chapter(_id, td.text.strip(), url + td.a.attrs['href']))
        return chapters

    def __parse_chapter_content(self, html):
        bs_obj = BeautifulSoup(html)
        contents = bs_obj.find('dd', {'id': 'contents'})
        # print contents.text
        return contents.text

    def __add_chapter(self, chapter):
        try:
            self.collection.insert(chapter.dict())
        except:
            pass

    def __update_novel(self, novel):
        self.db.novels.update({'_id': novel._id}, {
            '$set': {'is_crawled': True},
        })
        self.collection.remove({'novel_id': novel._id})

    def __update_failed_novel(self, novel):
        self.db.novels.update({'_id': novel._id}, {
            '$set': {'success': False},
        })

    def __close(self):
        self.client.close()


crawler = ChapterCrawler()
crawler.run()
print "chatper_crawler has been finished."
