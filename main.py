import os

import requests
from bs4 import BeautifulSoup


def retrieve_posts(site, per_page=100):
    try:
        url = f"{site}/wp-json/wp/v2/posts?per_page={per_page}"
        headers = {
            "user-agent":
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        }
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()  # Raise an exception if the request was unsuccessful
    except requests.RequestException as e:
        print(f"Failed to retrieve posts: {e}")
        return []

    total_posts = int(resp.headers.get("x-wp-total", 0))
    total_pages = int(resp.headers.get("x-wp-totalpages", 0))
    print(f"{total_posts} posts with {total_pages} pages in total")

    posts = []
    print("Starting retrieval")
    for page in range(1, total_pages + 1):
        print(f"Retrieving page {page}...")
        if page > 1:
            url = f"{site}/wp-json/wp/v2/posts?per_page={per_page}&page={page}"
            resp = requests.get(url, headers=headers)
        for item in resp.json():
            p = {
                "id": item["id"],
                "link": item["link"],
                "date": item["date"],
                "title": item["title"]["rendered"],
                "content": item["content"]["rendered"]
            }
            posts.append(p)
    print(f"Retrieval finished. {len(posts)} posts retrieved")
    return posts


def get_data_from_post_page(html, url):
    soup = BeautifulSoup(html, "html.parser")
    title_element = soup.find("h1", class_='entry-title')
    if title_element is None:
        print(f"No title found at {url}. Skipping this page.")
        return "NoTitle", "NoContent"
    title = title_element.get_text(strip=True)
    content_element = soup.find("div", class_='entry-content')
    if content_element is None:
        print(f"No content found at {url}. Skipping this page.")
        return title, "NoContent"
    content = content_element.get_text(strip=True)
    return title, content


# def export_to_file(posts):
#     with open("posts.txt", "w") as f:
#         for post in posts:
#             f.write(f"{post['title']}\n{post['content']}\n\n")

def export_to_file(posts):
    # Create the directory if it doesn't exist
    if not os.path.exists('./export_html'):
        os.makedirs('./export_html')

    for post in posts:
        # Replace any characters in the title that are not allowed in file names
        safe_title = "".join(c for c in post['title'] if c.isalnum() or c in (' ',)).rstrip()
        filename = f"./export_html/{safe_title}_post.txt"
        with open(filename, "w", encoding='GBK') as f:
            f.write(f"{post['title']}\n{post['content']}\n\n")


def main():
    site = input("请输入wordpress站点地址：")
    per_page = input("请输入每页文章数量（默认100）：")
    if not per_page.isdigit():
        print("Invalid input. Using default value 100.")
        per_page = 100
    else:
        per_page = int(per_page)

    posts = retrieve_posts(site, per_page)
    for post in posts:
        print(f"Retrieving post {post['title']}...")
        title, content = get_data_from_post_page(post["content"], post["link"])
        # 输出到文件 调用export_to_file函数
        export_to_file(posts)
        print('获取成功，文章标题: ' + title)
        print("已获取文章内容")


if __name__ == '__main__':
    main()
