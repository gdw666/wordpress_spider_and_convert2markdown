import re
import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import pyperclip
import ssl

def main():
    url = input("Input stackoverflow question url: ")
    html = ask_url_get_html(url)
    print('Getting html file from url...')
    answer_num = 3
    answer_num = int(input('How many answers will be chosen(default:3): ')) or 3
    page_info = get_data_from_html(html, answer_num)
    print('Select the first 3 answers, processing...')
    wordpress_format = convert_to_wordpress_format(page_info, url)
    print('Success, the result will paste to the shear plate.')
    pyperclip.copy(wordpress_format)
    print('Copy success.')
    input("Press the ENTER key to close.")


def ask_url_get_html(url):
    #   从url中获取html文件
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    }
    request = urllib.request.Request(url, headers=head)
    html = None
    try:
        response = urllib.request.urlopen(request, context=ssl._create_unverified_context())
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    if html is None:
        input("Enter any key to continue")

    return html


def get_data_from_html(html, answer_num):
    #   html文本处理，收集标题、内容、作者名、作者主页链接、回答投票，得到并返回页面信息

    #   正则表达式
    find_title = re.compile('">(.*)</a>')
    find_description = re.compile('">(.*)</div>', re.DOTALL)
    find_author_name = re.compile('name">(.*?)</span>')
    find_author_link = re.compile('(href="(.*)">.*</a>)|(Person">(.*)<span)')
    find_vote_count = re.compile('data-value="(\d*?)"')

    soup = BeautifulSoup(html, "html.parser")
    #   标题匹配
    item = str(soup.find_all("a", class_="question-hyperlink", limit=1))
    title = re.findall(find_title, item)
    #   内容匹配，并修改/去除部分标签，方便后续处理
    item = str(soup.find_all("div", class_="s-prose js-post-body", limit=answer_num+2))
    item = item.replace("\n", "").replace('\r', '')
    item = item.replace('<ul>', '').replace('</ul>', '')
    item = item.replace('<li>', '').replace('</li>', '')
    item = item.replace("/pre>", "/p>").replace('<pre', '<p')
    item = item.replace("/p>", "/li>").replace("<p", "<li")
    # print(item)
    description = re.findall(find_description, item)
    description = description[0].split('</div>, <div class="s-prose js-post-body" itemprop="text">')
    #   作者名及作者连接匹配
    item = str(soup.find_all('div', class_="user-details", itemprop="author", limit=answer_num+1))
    # item = item.replace()
    author_name = re.findall(find_author_name, item)
    author_link = re.findall(find_author_link, item)\
    #   投票数匹配
    item = str(soup.find_all("div", class_='js-vote-count', limit=answer_num+1))
    vote_count = re.findall(find_vote_count, item)

    #   按序整理匹配信息
    page_info = []
    page_info.append(title[0])
    for pos in range(0, answer_num + 1):
        page_info.append(author_name[pos])
        if len(author_link) == answer_num + 1:
            page_info.append(author_link[pos][1])
        else:
            page_info.append("")
            if pos == 0: print('Link loss, maybe account cancellation?\nAll link replace with ""')
        page_info.append(description[pos])
        page_info.append(vote_count[pos])
    return page_info


def convert_to_wordpress_format(page_info, url):
    #   页面信息转WordPress格式文本
    wordpress_content = """
<blockquote class="wp-block-quote"><p><a rel="noreferrer noopener" 
href="https://mwhls.top/programming-language-learning/stackoverflow" 
target="_blank">stackoverflow热门问题目录</a></p><p>如有翻译问题欢迎评论指出，谢谢。</p></blockquote>
<!-- /wp:quote --><!-- wp:heading {"textAlign":"center","level":4} -->
<h4 class="has-text-align-center"><a rel="noreferrer noopener" href="
    """ + url + '" target="_blank">' + page_info[0] + '''</a></h4><!-- /wp:heading --><!-- wp:list --><ul><li><a rel="noreferrer noopener" href="https://stackoverflow.com''' + page_info[2] + '" target="_blank">' + page_info[1] + '''</a> asked:
    <ul>''' + page_info[3] + '</ul></li>' + '<li>Answers:'

    for pos in range(1, len(page_info) // 4):
        wordpress_content += '<ul><li><a rel="noreferrer noopener" href="https://stackoverflow.com'
        wordpress_content += page_info[4 * pos + 2]
        wordpress_content += '" target="_blank">'
        wordpress_content += page_info[4 * pos + 1]
        wordpress_content += '</a> - vote: '
        wordpress_content += page_info[4 * pos + 4]
        wordpress_content += '<ul>'
        wordpress_content += page_info[4 * pos + 3]
        wordpress_content += '</ul></li></ul>'

    wordpress_content += '</li></ul><!-- /wp:list -->'
    return wordpress_content


if __name__ == '__main__':
    main()
