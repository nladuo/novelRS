# novelRS
一个简单的网络小说推荐系统，写着玩儿。

## 状态
正在构建中。。。

## 小说数据
### 下载地址
链接: 待上传。。。。。

### 导入数据
``` shell
mongoimport -d novelRS -c novels  --file ./novels.dat
```

## 算法步骤
1、爬取数据<br>
2、使用jieba分词<br>
3、小说内容向量化<br>
4、转换为td-idf向量<br>
5、k-means聚类减小复杂度<br>
6、计算相似度<br>

## 安装
### 配置
修改lib/config.py
``` python
config = {
    'timeout': 3,
    'db_user': '',          # 无密码
    'db_pass': '',
    'db_host': 'localhost',
    'db_port': 27017,
    'db_name': 'novel_rs',
    'cpu_num': 4            # 并行分词的CPU数目
}
```

### 爬虫
``` shell
python crawler/novel_crawler.py     # 爬取小说
python crawler/chapter_crawler.py   # 爬去小说章节
```

### 推荐系统
``` shell
python RS/word_segmentation.py  # 爬取小说
python RS/get_vectorizer.py     # 爬去小说章节
python RS/vectorize.py          # 向量化
python RS/tdidf_transformer.py  # 转换为tf-idf向量
python RS/kmeans_cluster.py     # 聚类减小复杂度
python RS/similarity_counter.py # 计算相似度
```

### web服务
``` shell
cd web && npm install
npm build               # 构建前端
python main.py          # 启动web服务器
```

## TODO
- [ ] 1. 多核计算

## LICENSE
MIT