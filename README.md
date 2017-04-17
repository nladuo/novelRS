# novelRS
一个简单的网络小说推荐系统，写着玩儿。  
想法来源于: [一个简单的网文推荐系统，解决书荒](https://www.v2ex.com/t/308827)
## 状态
正在构建中.....

## 网站Demo
前端：vue+vuex <br>
后端：flask <br>
数据库：mongodb

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
4、k-means聚类减小复杂度<br>
5、计算相似度<br>

## 安装
### 配置
修改lib/config.py
``` python
config = {
    'timeout': 3,
    'db_user': '',          # mongo的用户名
    'db_pass': '',          # mongo的密码
    'db_host': 'localhost',
    'db_port': 27017,
    'db_name': 'novelRS',
    'cpu_num': 4            # 开几个进程
}
```

### 安装依赖
``` shell
pip install -r requirements.txt
```

### 爬虫
``` shell
python crawler/novel_crawler.py     # 爬取小说
python crawler/chapter_crawler.py   # 爬去小说章节
```

### 推荐系统
``` shell
python RS/word_segmentation.py  # 分词
python RS/vectorizer.py         # 向量化
python RS/kmeans_cluster.py     # 聚类减小复杂度, 此步骤大概需要6-7G内存
python RS/similarity_counter.py # 计算相似度
```

### 部署web服务
``` shell
cd web_demo && npm install
npm run build               # 构建前端
python main.py              # 启动web服务器
```


## LICENSE
MIT
