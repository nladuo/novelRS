# novelRS
一个简单的网络小说推荐系统。

## 状态
重新开发中......

## 开发环境
python3.6 + mongodb


## 代码说明
### 运行小说爬虫
下载小说列表：
```bash
cd crawler & python3 info_crawler.py
```
下载小说的txt：
```bash
cd crawler & python3 txt_downloader.py
```
小说过滤（只考虑大于500KB的小说）：
```bash
cd crawler & python3 download_check.py
```

### 运行推荐算法
通过ipython notebook打开RS.ipynb
```bash
cd RS && ipython3 notebook
```

### 网页Demo


## LICENSE
MIT
