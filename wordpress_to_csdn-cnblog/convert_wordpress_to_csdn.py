import re
import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import pyperclip


def main():
    mode = input("""
选择爬取模式：
1. 从归类页面中批量爬取文章，回车直接进入。
2. 从文章链接中爬取文章内容，输入文章链接进入。
    """)
    if mode == '':
        get_from_page()
    else:
        get_from_post(mode)
    print("转换成功，程序正常结束。")


def get_from_post(post_url):
    html = ask_url_get_html(post_url)
    html_data = get_data_from_post_page(html, post_url)
    print('获取成功，文章标题已粘贴至剪切板。')
    pyperclip.copy(html_data[0])
    input("按下回车复制文章内容。")
    pyperclip.copy(html_data[1])
    input("已获取文章内容，按下回车继续。")


def get_from_page():
    page_url = input("请输入页面地址（回车爬取首页）：")
    if page_url == '':
        page_url = "https://mwhls.top/"

    article_num = input("转换文章数（默认1，最多10）：")
    if article_num == '':
        article_num = 1
    else:
        article_num = int(article_num)

    html = ask_url_get_html(page_url)
    url = get_url_from_homepage(html, article_num)

    for pos in range(article_num - 1, -1, -1):
        print('第{0}篇文章的html文本获取中...'.format(article_num - pos))
        html = ask_url_get_html(url[pos])
        html_data = get_data_from_post_page(html, url[pos])
        print('获取成功，文章标题已粘贴至剪切板。')
        pyperclip.copy(html_data[0])
        input("按下回车复制文章内容。")
        pyperclip.copy(html_data[1])
        input("已获取文章内容，按下回车继续。")


def ask_url_get_html(url):
    #   从url中获取html文件
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
    }
    request = urllib.request.Request(url, headers=head)
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


def get_url_from_homepage(html, article_num):
    #   从主页中获得文章链接
    find_url = re.compile('href="(.*?)" rel=')
    soup = BeautifulSoup(html, "html.parser")
    item = str(soup.find_all("h2", class_='post-title', limit=article_num))
    url = re.findall(find_url, item)
    return url


def get_data_from_post_page(html, url):
    #   从文章页面获取信息并转换成CSDN格式
    find_content = re.compile('</div>(.*)]', re.DOTALL)
    find_title = re.compile('title">(.*)</h1>')
    soup = BeautifulSoup(html, "html.parser")
    item = str(soup.find_all("h1", class_='post-title'))
    title = re.findall(find_title, item)
    item = str(soup.find_all("div", class_='entry'))
    item = item.replace('<pre class="wp-block-code"><code>', '\n\n<!-- wp:code -->\n<pre class="wp-block-code"><code>')
    item = item.replace('</code></pre>', '</code></pre>\n<!-- wp:code -->\n')

    content = re.findall(find_content, item)
    content[0] = """
<p><em>文章首发及后续更新：<a href="{0}">{1}</a>，无图/无目录/格式错误/更多相关请至首发页查看。<br/> 
新的更新内容请到<a href="https://mwhls.top/">mwhls.top</a>查看。<br/> 
欢迎提出任何疑问及批评，非常感谢！</em></p>
    """.format(url, url) + content[0]
    html_data = []
    html_data.append(title[0])
    html_data.append(content[0])

    return html_data


if __name__ == '__main__':
    main()
