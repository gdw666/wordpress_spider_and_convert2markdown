> 博客：https://mwhls.top/2186.html
> 
> GitHub：https://github.com/asd123pwj/wordpress_spider
>
> *推荐参考：*[Python爬虫入门](https://mwhls.top/programming-language-learning/python-spider-base)
>
> 2022/4/5更新：适配了博客园格式，在**首页爬取模式**的基础上加入了**文章归类批量爬取模式**和**文章链接爬取模式**。

#### 项目介绍

- `convert_wordpress_to_csdn.py`
  - 爬取我的[WordPress博客](https://mwhls.top/)，并转换为CSDN格式、博客园可用格式。
    - CSDN直接粘贴。
      博客园使用`TextBox`编辑器。
  - 批量爬取首页的文章。
  - 批量爬取某个分类/标签/归档下的文章。
  - 根据文章链接爬取文章。
  - 为文章开头添加转载信息。
- `py2exe.py`
  - 与 `convert_wordpress_to_csdn.py` 放在同一目录下，运行后可生成exe文件。

#### 项目思路

- 思路和前一篇文章很像，我这里就介绍一下大概思路以及问题处理，其余不再赘述了。
  - 见：[Python爬取StackOverflow问题页面并转换为WordPress可用格式](https://mwhls.top/?p=2175)
1. 获取页面html文本
2. 从博客主页获取文章链接
  - 分割的时候，re总是匹配最多的内容，而这些内容之间又有变动的东西，不能像上篇文章一样用split分片。
    - 即，使用 ` href=(.*) ` 匹配时，它总是从第一个`href=`匹配到最后一篇文章的``。
  - 然后查了几个方法，试了用re的split，但依然是同样问题，虽然分割了，但还是把不该包括的东西也包括进去了。
  - 最后在re的官方文档里面找到了解决办法：
    - 加一个`?`，将 `(.*)` 改成 `(.*?)`，即可达到非贪婪匹配的效果，匹配最少的字符，
    - 见：[https://docs.python.org/zh-cn/3/library/re.html](https://docs.python.org/zh-cn/3/library/re.html)
3. 爬取上一步获取的链接对应的文章
     - 在转换成CSDN格式的时候，原本是打算用管理员账号的编辑模式页面，
     - 因为我一直都是用这个页面来发文章的。
     - 然后试了试直接爬取，可行，于是直接爬取。
     - 但在代码格式的处理中有问题，如果连续空两行，就会出问题。
     - 最后在代码标签前后加上了WordPress的code标签才解决。
4. 输出结果
