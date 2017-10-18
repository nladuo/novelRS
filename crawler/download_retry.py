# coding=utf-8
""" 重新下载大小小于100K的小说(由于下载失败导致的) """
from __future__ import print_function
import time
import sys
sys.path.append("../")
from lib.utils import *
from lib.config import *
import urllib
import os.path


reload(sys)
sys.setdefaultencoding('utf8')

def reporthook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration))
    percent = min(int(count * block_size * 100 / total_size), 100)
    sys.stdout.write("\r...%d%%, %d KB, %d KB/s, %d seconds passed" %
                    (percent, progress_size / 1024, speed, duration))
    sys.stdout.flush()

def need_download(novel):
    path = os.path.join('corpus', str(novel["_id"]) + ".txt")
    filesize = os.path.getsize(path)
    need = filesize < 50 * 1024 # 小于50KB要重新下载一遍

    if need:
        print(novel['_id'], novel['name'], "filesize:", filesize)

    return need

class TxtDownloader:
    """ 爬取小说的章节，存到数据库中 """
    def __init__(self):
        self.client = init_client()
        self.db = self.client[config['db_name']]
        self.novels = self.db.novels.find({})

    def run(self):
        novels = []
        # 先把数据都读到内存里
        for novel in self.novels:
            novels.append(novel)

        for novel in novels:
            if not need_download(novel):
                continue

            download_url = urllib.quote(str(novel['download_url'])).replace("http%3A", "http:")
            print("retry downloading", novel['_id'], novel['name'], novel['author'], novel["category"],
                  download_url)

            filename = os.path.join('corpus', str(novel['_id']) + ".txt")
            urllib.urlretrieve(download_url, filename, reporthook)

            print("\nSaved in", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))

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