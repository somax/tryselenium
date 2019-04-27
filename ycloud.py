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

def md5(str):
    return hashlib.md5(str.encode()).hexdigest()


api_url = 'http://0.0.0.0:3000/flows'

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# driver = webdriver.Chrome('/Users/mxj/Downloads/chromedriver')
# driver = webdriver.Chrome('/Users/mxj/Downloads/chromedriver_73.0.3683.68')
driver = webdriver.Chrome('/Users/mxj/Downloads/chromedriver_74.0.3729.6')

# need copy geckodriver to /usr/local/bin
# driver = webdriver.Firefox()


driver.implicitly_wait(10)
wait = WebDriverWait(driver, 10)
action = ActionChains(driver)

#====== 定义快捷方法 ========

def find(xpath):
    return wait.until(EC.presence_of_element_located((By.XPATH, xpath)))


def finds(xpath):
    return driver.find_elements_by_xpath(xpath)


def findchild(el, xpath):
    return el.find_element_by_xpath(xpath)


def findchildren(el, xpath):
    try:
        _el = el.find_elements_by_xpath(xpath)
    except:
        sleep(2)
        _el = el.find_elements_by_xpath(xpath)
    return _el


def findlink(text):
    return driver.find_element_by_link_text(text)


def switchtoframe(name):
    driver.switch_to.frame(name)


# 定义 点击 方法
def click(xpath, delay=1):
    find(xpath)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    element.click()
    sleep(delay)


# 定义 输入字符 方法
def sendkeys(xpath, keys, delay=.5):
    wait.until(EC.presence_of_element_located((By.XPATH, xpath))).send_keys(keys)
    # driver.find_element_by_xpath(xpath).send_keys(keys)
    sleep(delay)


def waitfor(xpath):
    # 等待登录
    while True:
        try:
            find(xpath)
            print("继续")
            break
        except:
            print("等待...", xpath)
            sleep(1)


def switchtowindow(id):
    driver.switch_to.window(driver.window_handles[id])


def close():
    driver.close()


# 全屏
driver.fullscreen_window()




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


companies = ['上海翌洲物业管理有限公司','上海永菱房产发展有限公司','上海尚敏管理咨询有限公司']

# TODO issue 目前完成第一家公司后不能定位下拉菜单, 只能一家一家来: 改 range
for k in range(2,3):

    company = companies[k]

    # 重置焦点 TODO 
    # switchtowindow(0)
    # driver.switch_to.default_content()
    # driver.switch_to.parent_frame()

    #======= 切换空间 =======
    # click("//span[@class='fs-qz-dropdown-link']",1)
    # 改成鼠标移动到上面打开下拉菜单了
    ele_dropdown=find("//span[@class='fs-qz-dropdown-link']")
    sleep(2)
    action.move_to_element(ele_dropdown).perform()
    # click("/html/body/div[2]/div[1]/div/div[1]/header/div/div[2]",1)
    sleep(2)
    # driver.execute_script("document.getElementsByClassName('fs-header-drop-menu')[0].style.display = '';")

    click('//li/span[contains(text(),"' + company + '")]')



    #======= 切换到数据列表 =======
    # 点击 审批
    click('//div[@title="审批"]')

    # 点击 BPM后台
    switchtoframe(0)
    click('//span[contains(text(),"BPM后台")]')


    # 点击 流程调度

    switchtoframe(0)
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
    # page_count=1 # TODO for debug
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
        

        # --- 取数据
        sleep(2)
        rows = finds('//div[@class="fs-table__body-wrapper"]/table/tbody/tr')
        for o in range(0,len(rows)):
            sleep(2)
            # items = []
            _flow_formdata = {}
            cells = findchildren(rows[o],'.//td')

            # 取出列表中的值,取第2列到第7列
            for j in range(1,7):
                _flow_formdata[headitems[j]] = cells[j].text

            # 获得单据号
            _flowid = md5(cells[6].text)


            # 流程调度列表中点击 单据号
            cells[6].click()

            # 切换到打开的窗口
            switchtowindow(1)

            # --- 获取表单值 ---
            # 获得流程
            # _flowstep = find('//*[@id="app"]/div/div/div[2]/div[1]').text.replace('\n', '； ')
            sleep(3)
            _flowstep = find('//div[@class="process-preview"]').text.replace('\n', '； ')
            _flow_formdata['流程进度'] = _flowstep

            # 找到所有字段的容器
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
                        _text = _ele_v.get_attribute('textContent')
                    else:
                        _text = _ele_v.text

                print(_text)

                _flow_formdata[_title]=_text

            # _flows.append(_flow_formdata)

            print('post to database...')
            _flow_formdata['id'] = _flowid
            _flow_formdata['_time'] = str(datetime.datetime.now())
            _flow_formdata['公司名称'] = company
            res = req.post(api_url, data=_flow_formdata)

            # 如果记录以及存在, 则尝试更新数据
            if not res.ok and ('duplicate id' in res.text):
                res = req.put(api_url + '/' + _flowid, data=_flow_formdata)
            
            print(res.status_code, res.reason)

            # print(_flows)



            # 关闭并返回列表窗口
            driver.close()
            switchtowindow(0)

            # 切换 frame 重新来一遍,保证不出错
            driver.switch_to.parent_frame()
            switchtoframe(0)
            switchtoframe(0)





# ----- DONE -----
print('DONE')

driver.close()
