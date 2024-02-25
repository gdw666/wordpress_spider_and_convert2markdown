> 博客：https://mwhls.top/2175.html
>
> GitHub：https://github.com/asd123pwj/wordpress_spider
>
> 推荐参考：[Python爬虫入门](https://mwhls.top/programming-language-learning/python-spider-base)
>
> 这篇文章是在做出来后第六天写的， 写着写着我又想写爬虫了，因此又写了个WordPress转CSDN的，就不用我每次加前缀了。 python真好用噢。
>
> 2021/9/11更新：代码更新，增加处理注销用户的功能。
>  
> 2021/9/21更新：代码更新，修复十天前加上的bug。
> 
> 2021/10/2更新：代码更新，修复十一天漏掉的bug。增加数量选择。
> 
> 2022/4/5更新：修改介绍，添加GitHub链接，添加转为exe的代码。

#### 项目介绍

- `stackoverflow_spider.py`
  - 爬取StackOverflow问答，转为WordPress格式
  - 示例：[译（五十三）-Pytorch的stack()与cat()有何区别](https://mwhls.top/3727.html)
- `py2exe.py`
  - 与`stackoverflow_spider.py`同一目录下，运行后生成exe文件。

#### 在中间的前言

- 现在开了个栏目，翻译StackOverflow文章。
- 但每次转换有点麻烦，复制粘贴改格式。
- 于是就有了这篇。
- 输入StackOverflow的问题网址，爬取后，转换成我的行文格式，并自动复制到剪切板。
- 值得一提的是，WordPress的格式与html的格式还是挺像的，所以不需要做太大的改变。
- 最后的成果也不错，只有两个问题： 
  - 链接不是在新页面打开，而是在当前页面打开，这就要求我每次手动修改，但也只是十几秒的时间。
  - `这里`的内容没有换行符，所以转换过来还需要我自己加，但我选的问题都是我能看懂的，所以加点换行符也不是大问题。

#### 项目思路

1. 爬取网页


  - 使用了urllib库。
  - 相关函数是`ask_url_get_html(url)`
  - 是很基础的用法，因为只爬取这一个页面，还是不用登陆就可以看到的页面，所以连cookie都不需要。
  - 提交一个链接后，爬取它的html文本。

2. 网页与WordPress文章格式分析


  - 用到了BeautifulSoup库、re库。
  - 相关函数是`get_data_from_html(html, answer_num)`
  - 首先我的文章需要几个部分：
  - 标题及其链接。
  - 提问者ID，提问内容，提问者主页链接。
  - 回答者ID，回答内容，回答者主页链接，投票数。
  - 回答数量。 
    - 这个后来删去了，爬取倒不是说麻烦，但就是想偷懒。
  - 然后就是观察在页面的哪些部分：
  - 先是比较简单的： 
    - 标题： 
          - 很容易获取，游览器右键审查元素找到的就是它。
          - 或者bs4的title也能获取。
    - 标题链接： 
          - 这个是我给它的，所以不用获取。
    - 提问者ID： 
          - 右键审查元素，它的类是‘user-details’。
    - 提问内容： 
          - 类是‘s-prose js-post-body’。
    - 提问者链接： 
          - 和前面提问者ID在一起。
  - 来到了回答者的部分，就比较麻烦了： 
    - ID、内容、主页、投票数，它们的类与提问者都一致。
    - 也就是说，找到的第一个并不是我们需要的。
    - 但这还好，用re表达式匹配后，变成列表后也可以直接取得，所以还好。
  - 更麻烦的是内容匹配，因为有换行符，所以re不能完全匹配上所有内容，只有第一句。 
    - 后来尝试了几个函数，最后使用`str.replace(\n, ).replace('\r', '')`以及`re.DOTALL`来删除所有换行符。
    - 然后可以正常匹配到完整内容了，但因为匹配用的表达式，会用上与下一个内容的标签，所以在匹配的时候需要多匹配一个内容。 
          - 即，如果我要找第三个回答，因为提问内容标签与回答标签一致，
          - 第三个回答实际上是第四个内容，
          - 并且还因为要用到下一个内容的标签来匹配，所以实际上要匹配五个内容，
          - 才能找到第三个回答的内容。
  - 之后是转换成WordPress格式：
  - 只有内容需要转换，其他像ID、主页这些信息，实际上只是拼接而已。
  - 就来测试获取的能不能直接用： 
    - 测试后发现可以，内容中`代码`的内容，恰好也是WordPress的代码块格式。
    - 所以匹配到的东西，复制粘贴就能用。
  - 但因为我是用WordPress里的列表来展示的，所以还需要进一步转换： 
    - 选择一句复制粘贴来的内容，转换成WordPress列表，然后复制这个区块来分析。
    - 发现与html格式类似，是加了前缀与后缀，然后多个标签。
  - 大部分的内容是能直接用的，但如果回答者以代码块开头，就会导致格式出错： 
    - StackOverflow里的代码块用到了，
    - 而每次我给WordPress列表添加内容的时候，还会加上
    - 就使得WordPress列表的第一行会直接向右移动两个缩进。 
          - 有点像首行缩进，正常两个字符。
          - 而两个会导致四个字符作为首行缩进。
    - 但WordPress不允许这种情况出现，就会导致格式损坏。 
          - 而且我也不可能用这么丑的格式。
    - 最终在这里的格式处理比较麻烦，有的格式不报错，但是不能正常显示。
    - 最后还是用较为复杂的内容转换成WordPress列表，加上换行和缩进，再一行行比较。

3. 格式转换


     - 相关函数是`convert_to_wordpress_format(page_info, url)`


     - 就是字符串拼接。


     - 主要的难点在列表格式生成。


     - 这点就是前面最后内容匹配讲的。


     - 最后是用爬取到的内容，转换成WordPress列表格式，加上换行与缩进，再与自己生成的格式一行行比较。

4. 输出为可用格式


     - 用到了pyperclip库。


     - 测试的时候使用print输出的，然后复制粘贴，但太过麻烦。


     - 于是选择转换成文本，但从pycharm文本中复制的内容，虽然和WordPress需要的格式一模一样吧，但是不会自动转换。


     - 于是找了一个pyperclip库，可以将文本粘贴至剪切板。


     - 虽然每次爬取页面后必须要及时粘贴吧，但也不是麻烦事。


     - 即便希望在处理后自行选择是否粘贴，也只需要加个选项，循环这个粘贴函数就好了。


     - 所以这个项目就大功告成了。

5. 转换成exe文件

     - 用pyinstaller将文件转换成exe文件，避免每次都需要打开pycharm。