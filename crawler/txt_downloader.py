# coding=utf-8
from __future__ import print_function
import time
import sys
sys.path.append("../")
from lib.utils import *
from lib.config import *
import urllib
import os.path
import socket
socket.setdefaulttimeout(5)


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
            download_url = urllib.quote(str(novel['download_url'])).replace("https%3A", "https:")
            print("downloading", novel['_id'], novel['name'], novel['author'], novel["category"],
                  download_url)

            filename =  os.path.join('corpus', str(novel["_id"]) + ".txt")
            success = False
	    while not success:
		try:
	            urllib.urlretrieve(download_url, filename, reporthook)
		    success = True
		except IOError:
		    print("timeout error")

            print("\nSaved in", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
            self.__update_novel(novel)  # 把novel的is_downloaded设为1
	    time.sleep(1)

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
