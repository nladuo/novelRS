# coding=utf-8
from gevent import monkey; monkey.patch_all()
import gevent
from gevent import queue
import time
from bs4 import BeautifulSoup
import sys
sys.path.append("../")
from lib.utils import *
from lib.model import *
from lib.config import *


reload(sys)
sys.setdefaultencoding('utf8')


class ChapterCrawler:

    def __init__(self):
        self.client = init_client()
        self.db = self.client[config['db_name']]
        self.novels = self.db.novels.find({'is_crawled': False})

    def run(self):
        novels = []
        # 先把数据都读到内存里
        for novel in self.novels:
            n = Novel(
                novel['name'],
                novel['author'],
                novel['category'],
                novel['word_num'],
                novel['url'],
                novel['is_crawled'],
                novel['success'],
                novel['is_segment'],
                novel['is_compute']
            )
            n._id = novel['_id']
            novels.append(n)

        for novel in novels:
            print "scraping", novel._id, novel.name, novel.author, \
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            html = get_body(novel.url)
            pre_chapters = self.__parse_chapters(novel._id, novel.url, html)
            # 小于300章的小说不进行统计，把novel的success设为0
            if len(pre_chapters) <= 300:
                self.__update_failed_novel(novel)
                continue
            tasks = []
            q = gevent.queue.Queue()
            chapter_count = 0
            for chapter in pre_chapters:
                tasks.append(gevent.spawn(self.__async_get_chapter_content, chapter, q))
                chapter_count += 1
                if chapter_count > 50:      # 节省硬盘，每本小说只爬取前50章
                    break
            gevent.joinall(tasks)

            novel_content = ''
            while not q.empty():
                dict = q.get()
                body = dict['body']
                chapter = dict['chapter']
                if len(body) == 0:
                    add_failed_url(self.db, chapter.url)
                    continue
                try:
                    content = self.__parse_chapter_content(body)
                    novel_content += content
                except:
                    pass
            self.__save_novel(novel, novel_content)
            self.__update_novel(novel)  # 把novel的is_crawled设为1

        self.__close()

    def __update_novel(self, novel):
        self.db.novels.update({'_id': novel._id}, {
            '$set': {'is_crawled': True},
        })

    def __update_failed_novel(self, novel):
        self.db.novels.update({'_id': novel._id}, {
            '$set': {'success': False},
        })
        self.__update_novel(novel)

    def __close(self):
        self.client.close()

    @staticmethod
    def __split_pre_chapters(pre_chapters, num=100):
        return [pre_chapters[i: i + num] for i in range(len(pre_chapters)) if i % num == 0]

    @staticmethod
    def __async_get_chapter_content(chapter, q):
        body = get_body(chapter.url)
        q.put({'chapter': chapter, 'body': body})
        print chapter.url

    @staticmethod
    def __parse_chapters(_id, url, html):
        chapters = []
        bs_obj = BeautifulSoup(html)
        tds = bs_obj.find_all('td', {'class', 'L'})
        for td in tds:
            if td.text.strip() != '':
                chapters.append(Chapter(_id, td.text.strip(), url + td.a.attrs['href']))
        return chapters

    @staticmethod
    def __parse_chapter_content(html):
        bs_obj = BeautifulSoup(html)
        contents = bs_obj.find('dd', {'id': 'contents'})
        # print contents.text
        return contents.text

    @staticmethod
    def __save_novel(novel, novel_content):
        filename = str(novel._id) + ".txt"
        f = open('./corpus/' + filename, 'w')
        f.write(novel_content)
        f.close()
        print "saving ", './corpus/' + filename

if __name__ == '__main__':
    crawler = ChapterCrawler()
    crawler.run()
    print "chatper_crawler has been finished."
