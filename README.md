# novelRS
一个简单的网络小说推荐系统。

## 状态
重新开发中......

## 开发语言
python2.7

<<<<<<< HEAD
=======
## 网站Demo
前端：vue <br>
后端：flask <br>
数据库：mongodb

## 小说数据
### 下载地址
链接: https://pan.baidu.com/s/1slTSiQT 密码: 2n3y

### 导入数据
导入数据后，即可在本地正常显示web_demo。
``` shell
mongoimport -d novelRS -c novels  --file ./novels.dat
```

## 运作流程
- 1、爬取数据<br>
- 2、对小说分词<br>
- 3、对分词后的小说进行TF-IDF向量化<br>
- 4、最近邻查找<br>
- 5、保存相似度到数据库<br>

## 安装
### 配置
修改lib/config.py
``` python
config = {
    'timeout': 3,
    'db_user': '',          # mongodb的用户名
    'db_pass': '',          # mongodb的密码
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
说明:这里只爬取了章节数目多于300章的小说
``` shell
cd crawler
python novel_crawler.py     # 爬取小说名称信息
python chapter_crawler.py   # 爬取小说章节保存到本地(1M带宽的服务器差不多得爬个半天)
```

### 推荐系统
测试服务器配置: 阿里云8G内存
``` shell
cd RS
python word_segmentation.py         # 分词, 跑了13多个小时
python vectorizer.py                # TF-IDF向量化, 大概半个小时
python lshf.py                      # 使用Locality Sensitive Hashing做最近邻查找, 大约一分钟
python similarity_computation.py    # 保存相似度到数据库
```

### 部署web服务
``` shell
cd web_demo && npm install
npm run build               # 构建前端
python main.py              # 启动web服务器
```

## TODO
- [ ] 支持并行分词
- [ ] 支持在线学习

>>>>>>> d1c89e5fe74cc909059c045815cf1f23cea14dba
## LICENSE
MIT
