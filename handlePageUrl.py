import re

def getUrlAndTitle(html_url):
    # 写一个正则表达式匹配所有符合'href="//www.zhihu.com/question/{question_id}/answer/{answer_id}">{questions_title}</a>'的字符串
    pattern = re.compile(r'href="//www.zhihu.com/question/\d+/answer/\d+">.*?</a>')

    url_title_list = []

    # 读取html文件
    with open(html_url, 'r', encoding='utf-8') as f:
        html = f.read()
        # 找到所有符合正则表达式的字符串
        matches = pattern.findall(html)
        # 遍历所有匹配结果
        for match in matches:

            # 从匹配结果中提取链接和题目
            url = match.split('">')[0].replace('href="//', 'https://')
            title = match.split('">')[1].replace('</a>', '')
            url_title_list.append((url, title))

    return url_title_list