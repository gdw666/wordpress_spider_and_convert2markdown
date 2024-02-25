# 爬取 Wordpress 网站的文章 并保存到本地

从 https://github.com/asd123pwj/wordpress_spider.git 受到启发，我也想写一个爬取 Wordpress 网站的文章的爬虫。

区别是，我想把爬取到的文章保存到本地，并且保存为 markdown 文件。

## Usage

爬取文章并提取 html 的主体内容

```bash
pip install -r requirements.txt
python main.py
```

### 转换为 markdown 文件

需要先运行 `main.py` 爬取文章，然后运行 `convert2markdown.py` 转换为 markdown 文件。

```bash
python convert2markdown.py
```

> 我使用的是 python3.9，之所以写这个爬虫让我受到启发的项目在我这里运行不了...
> 但是我觉得这个项目的思路很好，所以我写了这个项目。
