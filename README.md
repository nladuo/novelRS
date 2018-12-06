# novelRS
一个简单的网络小说推荐系统。

## 开发环境
python3.6 + mongodb

## 代码说明
### 运行小说爬虫
下载小说列表：
```bash
cd crawler & python3 info_crawler.py
```
下载小说的txt文件：
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
cd RS & ipython3 notebook
```
然后逐步运行：
- 1、分词
- 2、词表分析
- 3、TF-IDF构建
- 4、KD-Tree最近邻查询
- 5、相似度更新
### 网页Demo
```bash
cd web_demo & python3 main.py
```
运行后，打开[http://localhost:38438](http://localhost:38438)。
## LICENSE
MIT
