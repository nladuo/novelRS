# novelRS
一个简单的网络小说推荐系统，写着玩儿。想法来源于: [v2ex](https://www.v2ex.com/t/308827)
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

## 运作流程
- 1、爬取数据<br>
- 2、对小说分词<br>
- 3、对小说进行TF-IDF向量化<br>
- 4、使用k-means聚类把小说分为多个簇<br>
- 5、对同一簇(或最近邻簇)的小说计算余弦相似度<br>

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
python crawler/chapter_crawler.py   # 爬去小说章节(1M带宽的服务器差不多得爬个半天)
```

### 推荐系统
``` shell
python RS/word_segmentation.py      # 分词, 跑了13个多小时
python RS/vectorizer.py             # 向量化
python RS/kmeans_clustering.py      # 聚类减小复杂度
python RS/similarity_computation.py # 计算相似度
```

### 部署web服务
``` shell
cd web_demo && npm install
npm run build               # 构建前端
python main.py              # 启动web服务器
```

## TODO
- [ ] 支持并行分词
- [ ] 使用TF-IDF向量化
## LICENSE
MIT
