# coding=utf-8
""" 标记下载大小小于400K的小说 """
from __future__ import print_function
from lib.utils import *
from lib.config import *
import os.path


def check_download(novel):
    path = os.path.join('corpus', str(novel["_id"]) + ".txt")
    try:
        filesize = os.path.getsize(path)
        success = filesize >= 500 * 1024  # 保留大于500KB的小说
        print(novel['_id'], novel['name'], "filesize:", filesize, "success:", success)

        return success
    except:
        return False


class DownloadChecker:
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
            success = check_download(novel)
            self.__update_novel(novel, success)

        self.__close()

    def __update_novel(self, novel, success):
        """ 把小说设置为已经爬去取过 """
        self.db.novels.update({'_id': novel['_id']}, {
            '$set': {'is_saved': success},
        })

    def __close(self):
        """ 关闭数据库 """
        self.client.close()


if __name__ == '__main__':
    checker = DownloadChecker()
    checker.run()
    print("DownloadChecker has been finished.")

