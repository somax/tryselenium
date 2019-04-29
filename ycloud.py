#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

##################
# 友空间 数据爬取
##################

import csv
import json
import datetime
import requests as req
from os import environ
from time import sleep
import hashlib
import traceback

def md5(str):
    return hashlib.md5(str.encode()).hexdigest()


api_url = 'http://0.0.0.0:3000/flows'

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Chrome 则必须写全路径, Chrome 还需要注意版本和浏览器匹配, 下载地址 https://sites.google.com/a/chromium.org/chromedriver/home
driver = webdriver.Chrome('/usr/local/bin/chromedriver')

# Firefox 的驱动文件 geckodriver 需要复制到 /usr/local/bin/ 目录下，并且代码里不能配置路径，
# driver = webdriver.Firefox()


driver.implicitly_wait(10)
wait = WebDriverWait(driver, 10)
action = ActionChains(driver)

#====== 定义快捷方法 ========

def find(xpath):
    # return wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    while True:
        try:
            return driver.find_element_by_xpath(xpath)
            break
        except:
            print("重试定位元素...", xpath)
            sleep(1)


def finds(xpath):
    # return driver.find_elements_by_xpath(xpath)
    while True:
        try:
            return driver.find_elements_by_xpath(xpath)
            break
        except:
            print("重试定位元素们...", xpath)
            sleep(1)


def findchild(el, xpath):
    # return el.find_element_by_xpath(xpath)
    while True:
        try:
            return el.find_element_by_xpath(xpath)
            break
        except:
            print("重试定位子元素...", xpath)
            sleep(1)


def findchildren(el, xpath):
    # try:
    #     _el = el.find_elements_by_xpath(xpath)
    # except:
    #     sleep(2)
    #     _el = el.find_elements_by_xpath(xpath)
    # return _el
    while True:
        try:
            return el.find_elements_by_xpath(xpath)
            break
        except:
            print("重试定位子元素们...", xpath)
            sleep(1)


def findlink(text):
    return driver.find_element_by_link_text(text)


def switchtoframe(xpath):
    while True:
        try:
            _element = driver.find_element_by_xpath(xpath)
            sleep(1)
            driver.switch_to.frame(_element)
            break
        except:
            # traceback.print_exc()
            print("重试切换 frame...", xpath)
            sleep(1)


# 定义 点击 方法
def click(xpath, delay=1):
    # element = find(xpath)
    # element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    while True:
        try:
            driver.find_element_by_xpath(xpath).click()
            break
        except:
            # traceback.print_exc()
            print("重试点击...", xpath)
            sleep(1)
    # element.click()
    # sleep(delay)


# 定义 输入字符 方法
def sendkeys(xpath, keys, delay=.5):
    # wait.until(EC.presence_of_element_located((By.XPATH, xpath))).send_keys(keys)

    # sleep(delay)
    while True:
        try:
            return driver.find_element_by_xpath(xpath).send_keys(keys)
            break
        except:
            print("重试填入文字...", xpath, keys)
            sleep(1)


def waitfor(xpath):
    # 等待登录
    while True:
        try:
            find(xpath)
            print("继续")
            break
        except:
            traceback.print_exc()
            print("等待...", xpath)
            sleep(1)


def switchtowindow(id):
    driver.switch_to.window(driver.window_handles[id])


def close():
    driver.close()


# 全屏
# driver.fullscreen_window()




# =================================
print("opening yonyoucloud...")

# driver.get('https://ec.yonyoucloud.com/')
driver.get('https://ec.diwork.com/')


#======= 登录 =======
click("//a[contains(text(),'登录')]")
# 先在命令行设置环境变量：export YC_MOBILE=xxxxxx && export YC_PASSWORD=xxxxxxx

# LOGIN_USER = environ['YC_MOBILE']
# LOGIN_PASS = environ['YC_PASSWORD']

# TODO 临时设置，提交代码时清除
LOGIN_USER = ''
LOGIN_PASS = ''

sendkeys("//input[@name='mobile']", LOGIN_USER)
sendkeys("//input[@name='password']", LOGIN_PASS + '\n')



# 开始

flowStatus = "全部"

# 本地调试文件
# driver.get('file:///Users/mxj/tryselenium/html/%E9%9D%9E%E5%90%88%E5%90%8C%E4%BB%98%E6%AC%BE.html')

# TODO 用户测试或者断线续抓,或者补抓某些页码数据, _end_page 大于实际页数时按实际页数来.
_start_page = 0
_end_page = 1

companies = ['上海翌洲物业管理有限公司','上海永菱房产发展有限公司','上海尚敏管理咨询有限公司']

# TODO issue 目前完成第一家公司后不能定位下拉菜单, 只能一家一家来: 改 range
# for k in range(0,len(companies)):
for company in companies:

    #======= 切换空间 =======
    print('切换到空间:', company)

    # 改成鼠标移动到上面打开下拉菜单了
    while True:
        try:
            # 通过修改 css 样式直接将下拉菜单显示
            driver.execute_script("document.getElementsByClassName('fs-header-drop-menu')[0].style.display = '';")
            sleep(1)
            _menu_item = find('//li/span[contains(text(),"' + company + '")]')
            driver.execute_script("arguments[0].click();", _menu_item)
            # 点击完成后要立即隐藏,否则会遮挡后面链接,造成无法点击
            break
        except:
            sleep(1)
            driver.switch_to.parent_frame()
            traceback.print_exc()

    try:
        driver.execute_script("document.getElementsByClassName('fs-header-drop-menu')[0].style.display = 'none';")
    except:
        print('...')


    #======= 切换到数据列表 =======
    # 点击 审批
    click('//div[@title="审批"]')

    # 点击 BPM后台
    switchtoframe('//div[@class="fs-content-main"]/iframe')
    click('//span[contains(text(),"BPM后台")]')


    # 点击 流程调度
    switchtoframe('//div[@id="content"]/iframe')
    click('//span[contains(text(),"流程调度")]')

    click('//*[@id="app"]/div[2]/div/div/div[1]/div[3]/div[1]/input') # 20190424 改版下拉选项
    click('//span[contains(text(),"' + flowStatus + '")]')


    #======= 获取数据 =======
    # 将数据写入文件
    today = datetime.datetime.today().strftime('%Y%m%d')
    

    # 标题栏
    headitems = []
    headcell = finds('//div[@class="fs-table__header-wrapper"]/table/thead/tr/th')

    for i in range(0,len(headcell)):
        headitems.append(headcell[i].text)


    page_count = int(find('//li[contains(@class,"number")][last()]').text)

    # TODO 限定页数,用于测试,或者补抓取某几页数据
    if _end_page < page_count:
        page_count = _end_page

    print("总页数：",page_count)

    # 用来存储所有流程数据
    _flows = []


    for i in range(1, page_count+1):

        # --- 翻页
        if i > 1:
            xpath_next = "//div[@class='fs-pagination']//li[contains(text(),'" + str(i) + "')]"
            try:
                click(xpath_next)
            except:
                sleep(1)
                click(xpath_next)
        
        # TODO 如果中断,通过设置 _start_page 来快速跳过
        if i < _start_page:
            continue


        # --- 取数据
        sleep(1)
        rows = finds('//div[@class="fs-table__body-wrapper"]/table/tbody/tr')
        for o in range(0,len(rows)):

            # TODO for debug
            if o > 0:
                break

            # sleep(1)
            # items = []
            _flow_formdata = {}
            cells = findchildren(rows[o],'.//td')

            # 取出列表中的值,取第2列到第列7
            for j in range(1,7):
                _flow_formdata[headitems[j]] = cells[j].text

            # 获得单据号
            _flowid = md5(cells[6].text)


            # 流程调度列表中点击 单据号
            cells[6].click()

            # 切换到打开的窗口
            switchtowindow(1)

            # --- 获取表单值 ---

            # 找到所有字段的容器
            # sleep(1)
            ele_contains = finds("//div[@id='pane-formcomps']//td//*[@class='comp-title']/..")

            for _ele in ele_contains:

                # 在第一个div 中获得标签名称
                _ele_t = _ele.find_element_by_tag_name('div')
                _title = _ele_t.text.replace('* ','')
                print(_title)



                # 获得表单内容
                if '附件' in _title:
                    _text = _ele.text.replace(_title+'\n','').replace(' .','.').replace('\n','; ')
                else:
                    _ele_v = _ele.find_element_by_xpath('.//input | .//textarea | .//span[@class="file-name"]')

                    if _ele_v.tag_name == 'input':
                        _text = _ele_v.get_attribute('value')
                    elif _ele_v.tag_name == 'textarea':
                        _text = _ele_v.get_attribute('value')
                    else:
                        _text = _ele_v.text

                print(_text)

                _flow_formdata[_title]=_text



            # 获得流程 
            # sleep(1)
            # _flowstep = find('//div[@class="process-preview"]').text.replace('\n', '； ')
            click('//div[@id="tab-process"]')

            _el_steps = finds('//div[@class="process-detail-gram"]/div[@class="pro-task-item"]')

            _flowsteps = []
            for _el_step in _el_steps:
                _flowsteps.append(_el_step.text.replace('\n', ' '))

            print(_flowsteps)

            _flow_formdata['流程进度'] = _flowsteps



            print('post to database...')
            _flow_formdata['id'] = _flowid
            _flow_formdata['_time'] = str(datetime.datetime.now())
            _flow_formdata['公司名称'] = company

            try:
                res = req.post(api_url, data=_flow_formdata)
                # 如果记录以及存在, 则尝试更新数据
                if res.ok:
                    print('数据添加成功!')
                else:
                    if 'duplicate id' in res.text:
                        print('记录已存在尝试更新...')
                        res = req.put(api_url + '/' + _flowid, data=_flow_formdata)
                        if res.ok:
                            print('数据更新成功!')
                        else:
                            print('数据更新失败:',res.status_code , res.reason)
                    else:
                        print('数据提交失败:',res.status_code , res.reason)
                    
            except:
                print('ERROR:连接数据库出错!')
                # traceback.print_exc()




            # 关闭并返回列表窗口
            driver.close()
            switchtowindow(0)

            # 切换 frame 重新来一遍,保证不出错
            driver.switch_to.parent_frame()
            switchtoframe('//div[@class="fs-content-main"]/iframe')
            switchtoframe('//div[@id="content"]/iframe')

    # 完成一个公司所有页的数据抓取后, 回到主 frame
    driver.switch_to.parent_frame()






# ----- DONE -----
print('DONE')

driver.close()
