# 读取markdown文件，删除其中的超链接

import os
import re
import stat

def removeHyperlinks(path):
    # 读取文件
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    # 删除类似"[abc](https://www.zhihu.com/searchxxxxx)"的超链接，但需要匹配"https://www.zhihu.com/search"，保留"abc"
    content = re.sub(r'\[([^\[\]]+)\]\(https://www.zhihu.com/search[^\(\)]+\)', r'\1', content)

    # 写入文件
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':

    selected_path = '.'
    while os.path.isdir(selected_path + '/'):
        # 列出当前文件夹有哪些文件夹和文件
        dir_list = os.listdir(selected_path + '/')
        for i, file in enumerate(dir_list):
            print(i, '\t', file)

        # 让用户选择文件夹
        selected_num = input('请选择序号：')
        dir_name = dir_list[int(selected_num)]
        selected_path += '/' + dir_name

    print('您选择的文件夹是：', selected_path)

    # 删除超链接
    removeHyperlinks(selected_path)

    # 把path文件的权限更改为可写
    os.chmod(selected_path, stat.S_IWRITE)
