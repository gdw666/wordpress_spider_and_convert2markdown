import os
import html2text


# 转换 html 为 markdown

def convert_html_to_markdown():
    # 读取 ./export_markdown 目录下的所有 .md 文件
    # 读取文件内容，转换为 markdown 格式，保存为 "文章标题.md" 文件
    # 调用 html2text.html2text() 函数转换 html 为 markdown
    # 保存到 ./export_markdown 目录下
    # Create the directory if it doesn't exist
    if not os.path.exists('./export_markdown'):
        os.makedirs('./export_markdown')

    for filename in os.listdir('./export_html'):
        if filename.endswith(".txt"):
            with open(f"./export_html/{filename}", "r", encoding='GBK') as f:
                title = f.readline().strip()
                content = f.read()
                # Replace any characters in the title that are not allowed in file names
                safe_title = "".join(c for c in title if c.isalnum() or c in (' ',)).rstrip()
                with open(f"./export_markdown/{safe_title}.md", "w", encoding='UTF-8') as f:
                    f.write(f"# {title}\n\n{html2text.html2text(content)}\n\n")


if __name__ == '__main__':
    convert_html_to_markdown()
    print('转换成功')
