# 爬取知乎指定用户主页的回答

## 使用方法

1. 在[这里](https://www.selenium.dev/zh-cn/documentation/webdriver/getting_started/install_drivers/#%E5%BF%AB%E9%80%9F%E5%8F%82%E8%80%83)下载`webdriver`，并根据你的系统把所下载的东西放到`./chromedriver_mac64`或者`./chromedriver_win32`中。
2. 进入欲爬取的用户主页，点击回答标签栏，如：https://www.zhihu.com/people/<欲爬取的知乎用户ID>/answers?page=<页数>
3. 按`F12`，把`body`标签的内容都复制到[pageHtml.html](./pageHtml.html)中。
4. 命令行运行 `python main.py` ，按提示输入内容后，即可开始爬取。
5. 爬取到的回答内容将会整理成`.md`文件保存到`./result`文件夹中。

## 注意
* 使用太频繁有可能被知乎检测到。
* `./removeHyperlinks.py`是用于清除知乎内置超链接的小脚本，与爬虫无关。