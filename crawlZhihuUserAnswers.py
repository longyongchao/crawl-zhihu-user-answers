from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import platform
import re


def get_answer(user_url):

    # 根据操作系统设置不同的驱动路径
    system_name = platform.system()
    if system_name == 'Darwin':
        # 如果是macOS系统
        chromedriver_path = './chromedriver_mac64/chromedriver'
    elif system_name == 'Windows':
        # 如果是Windows系统
        chromedriver_path = './chromedriver_win32/chromedriver.exe'

    options = webdriver.ChromeOptions()
    # 设置不弹出浏览器窗口
    # options.add_argument('--headless')
    # 处理SSL证书错误问题
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    # 忽略无用的日志
    options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])

    # 初始化 Chrome 浏览器驱动器
    driver = webdriver.Chrome(chromedriver_path, options=options)

    driver.implicitly_wait(5)
    driver.set_window_size(1000, 1000)

    # 加载用户主页
    driver.get(user_url)

    # 查找关闭登录按钮并单击 
    print('正在关闭登录弹窗......')
    close_login_dialog_link = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div/div/div[2]/button')))
    close_login_dialog_link.click()

    print('正在查找问题描述展开全部按钮是否存在，若存在则点击......')
    show_all_xpath_3 = '//*[@id="root"]/div/main/div/div/div[1]/div[2]/div/div[1]/div[1]/div[3]/div/div/div/button'
    show_all_xpath_4 = '//*[@id="root"]/div/main/div/div/div[1]/div[2]/div/div[1]/div[1]/div[4]/div/div/div/button'
    def is_element_exist(xpath_3, xpath_4):
        # 查找xpath_3或xpath_4之一是否存在
        try:
            driver.find_element(By.XPATH, xpath_3).click()
            return 3
        except:
            try:
                driver.find_element(By.XPATH, xpath_4).click()
                return 4
            except:
                return 0
    which_exist = is_element_exist(show_all_xpath_3, show_all_xpath_4)
    
    print('正在尝试获取问题描述......')
    try:
        if which_exist == 3:
            question_desc = driver.find_element(By.XPATH, '//*[@id="root"]/div/main/div/div/div[1]/div[2]/div/div[1]/div[1]/div[3]/div/div')
        elif which_exist == 4:
            question_desc = driver.find_element(By.XPATH, '//*[@id="root"]/div/main/div/div/div[1]/div[2]/div/div[1]/div[1]/div[4]/div/div')
        question_desc = question_desc.text
    except:
        question_desc = '该问题没有问题描述'

    # 滑动到页面底部
    print('正在滑动到页面底部......')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    print('正在尝试获取答主回答......')
    answer = driver.find_element(By.XPATH, '//*[@id="root"]/div/main/div/div/div[3]/div[1]/div/div[3]/div/div/div/div[2]/span[1]/div/div/span')

    # 获取元素answer元素中的text和figure标签中的src属性，要求text和src属性按先后顺序，而且假设src已经动态加载完成。
    answer_text = answer.text
    
    # 等待图片加载完成

    try:
        print('正在等待图片加载完成......')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'figure')))
        figure_list = answer.find_elements(By.TAG_NAME, 'figure')
        for i, figure in enumerate(figure_list):
            answer_text += f'\n![图片{i}](' + figure.find_element(By.TAG_NAME, 'img').get_attribute('data-default-watermark-src') + ')'
    except:
        pass

    try:
        # 定位date_xpath元素，如果元素不存在则等待10秒
        edited_date = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ContentItem-time'))).text
        # 用正则表达式提取"编辑于 2021-12-07 04:17"中的年月日。
        edited_date = re.findall(r'\d{4}-\d{2}-\d{2}', edited_date)[0]
    except:
        edited_date = '0000-00-00'

    return question_desc, answer_text, edited_date, driver