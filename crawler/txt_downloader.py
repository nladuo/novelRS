# coding=utf-8
from __future__ import print_function
import time
import sys
sys.path.append("../")
from lib.utils import *
from lib.config import *
import urllib


reload(sys)
sys.setdefaultencoding('utf8')


class TxtDownloader:
    """ 爬取小说的章节，存到数据库中 """
    def __init__(self):
        self.client = init_client()
        self.db = self.client[config['db_name']]
        self.novels = self.db.novels.find({'is_downloaded': False})

    def run(self):
        novels = []
        # 先把数据都读到内存里
        for novel in self.novels:
            novels.append(novel)

        for novel in novels:
            download_url = urllib.quote(str(novel['download_url'])).replace("http%3A", "http:")
            print("downloading", novel['_id'], novel['name'], novel['author'], novel["category"],
                  download_url)
            filename = './corpus/' + str(novel['_id']) + ".txt"
            urllib.urlretrieve(download_url, filename)

            print("saved in", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
            self.__update_novel(novel)  # 把novel的is_downloaded设为1

        self.__close()

    def __update_novel(self, novel):
        """ 把小说设置为已经爬去取过 """
        self.db.novels.update({'_id': novel['_id']}, {
            '$set': {'is_downloaded': True},
        })

    def __close(self):
        """ 关闭数据库 """
        self.client.close()

if __name__ == '__main__':
    crawler = TxtDownloader()
    crawler.run()
    print("txt_downloader has been finished.")