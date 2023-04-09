from handlePageUrl import getUrlAndTitle
from crawlZhihuUserAnswers import get_answer
import re
import time

def main():

    url_title_list = getUrlAndTitle('./pageHtml.html')

    i = 0
    print('即将爬取以下问题：\n')
    for url, title in url_title_list:
        i += 1
        print(f'{i}-' + title, '\n\t', url)
    
    len_question = len(url_title_list)
    print(f'\n一共{len_question}条回答\n')

    # 让用户决定是否爬取的开始位置
    start = input('请输入开始爬取的位置：')
    end = input('请输入结束爬取的位置：')
    url_title_list = url_title_list[int(start) - 1: int(end)]
    task_num = int(end) - int(start) + 1

    page = input('请输入页码：')

    # 遍历所有问题的链接和题目
    for url, title in url_title_list:

        # 计时
        start_time = time.time()

        task_num -= 1

        print('\n正在爬取问题：' + title + '......')
        desc, answer, edited_date, driver = get_answer(url)

        # 只保留question中的中文和数字
        file_name = ''.join(re.findall('[\u4e00-\u9fa5\d]', title))

        # 将question、desc和answer写入result文件夹下的markdown文件，其中question作为文件名, desc和answer作为文件内容.
        with open('./result/' + edited_date + '-PAGE' + page + '-' + file_name + '.md', 'w', encoding='utf-8') as f:
            f.write('[' + title + ']' + '(' + url + ')\n\n' + '[[#' + title + ']]\n\n' + '问题描述：\n' + desc + '\n\n' + '###### ' + title + '\n\n' + answer)

        driver.quit()

        # 计算耗时，按分钟算
        end_time = time.time()
        cost_time = (end_time - start_time)
        cost_time = round(cost_time, 2)

        print(f'爬取完成！耗时 {cost_time} 秒，剩余 {task_num} 条问题\n')


if __name__ == '__main__':
    main()


