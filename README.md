# novelRS
一个简单的网络小说推荐系统，写着玩儿。

## 状态
正在构建中，目前算法复杂度太高了。。。

## 小说数据
### 下载地址
链接: 待上传。。。。。

### 导入数据
``` shell
mongoimport -d novel_rs -c novels  --file ./novels.dat
```

## 安装
### 配置
修改lib/config.py
```
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
python crawler/novel_crawler.py
python crawler/chap

```

### 推荐系统

### web服务

## TODO
- [ ] 1. 使用TF-IDF对corpus向量化.
- [ ] 2. 分词时添加停用词.
- [ ] 3. 多核计算相似度

## LICENSE
MIT