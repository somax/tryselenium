#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

##################
# 友空间 数据爬取
##################

import csv
import datetime
from os import environ
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome('/Users/mxj/Downloads/chromedriver')


driver.implicitly_wait(10)
wait = WebDriverWait(driver, 10)

#====== 定义快捷方法 ========

def find(xpath):
    return wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    
def finds(xpath):
    return driver.find_elements_by_xpath(xpath)
    
def findchild(el, xpath):
    return el.find_element_by_xpath(xpath)
    
def findchildren(el, xpath):
    return el.find_elements_by_xpath(xpath)

def findlink(text):
    return driver.find_element_by_link_text(text)

def switchtoframe(name):
    driver.switch_to.frame(name)


# 定义 点击 方法
def click(xpath, delay=1):
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

driver.get('https://ec.yonyoucloud.com/')


#======= 登录 =======
click("//a[contains(text(),'登录')]")
# 先在命令行设置环境变量：export YC_MOBILE= && export YC_PASSWORD=

# LOGIN_USER = environ['YC_MOBILE']
# LOGIN_PASS = environ['YC_PASSWORD']

# TODO 临时设置，提交代码时清除
LOGIN_USER = ''
LOGIN_PASS = ''

sendkeys("//input[@name='mobile']", LOGIN_USER)
sendkeys("//input[@name='password']", LOGIN_PASS + '\n')


# 等待登录成功后主页加载
waitfor("//span[@class='fs-qz-dropdown-link']")
sleep(2)
#======= 切换空间 =======
click("//span[@class='fs-qz-dropdown-link']",1)

# company = "尚敏"
company = "永菱"
# company = "翌洲"
click('//li/span[contains(text(),"' + company + '")]')



#======= 切换到数据列表 =======
# 点击 审批
click('//div[@title="审批"]')

# 点击 BPM后台
switchtoframe('iframepage')
click('//span[contains(text(),"BPM后台")]')


# 点击 流程调度
switchtoframe(find('//*[@id="content"]/iframe'))
click('//span[contains(text(),"流程调度")]')

click('//span[contains(text(),"全部")]')

# driver.get('https://yb.yonyoucloud.com/iform_web/static/rt.html#/browse?_=1552484012862&page=iformBrowse&pk_bo=388e72eb-8b86-405f-8cc5-1fe691b9ef37&pk_boins=497475e9-f57b-41bd-9b30-e56e5dabaf78&appsource=approve&sysId=diwork&source=BpmCenter&sso=true')

flowtype = '重大事项申请'
flowheads = ['事项名称','制单人','事项描述','日期']

#======= 获取数据 =======
# 将数据写入文件
today = datetime.datetime.today().strftime('%Y%m%d')
# 取第二列到第四列
cellrange = range(1,5)
with open('export/export-' + company + '-' + today+ '.csv', mode='w') as export:
    export_writer = csv.writer(export, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # 标题栏
    headitems = []
    headcell = finds('//div[@class="fs-table__header-wrapper"]/table/thead/tr/th')
    for i in cellrange:
        headitems.append(headcell[i].text)

    headitems = headitems + ['流程进度','附件'] + flowheads
    export_writer.writerow(headitems)

    count = int(find('//li[contains(@class,"number")][last()]').text)
    print("总页数：",count)
    for i in range(1,count+1):

        # --- 翻页
        # TODO 要滚动到显示元素才能点击, 目前点击出错后等待1秒再次尝试
        # ActionChains(driver).move_to_element(driver.find_element_by_xpath("//div[@class='fs-pagination']")).perform()
        if i > 1:
            xpath_next = "//div[@class='fs-pagination']//li[contains(text(),'" + str(i) + "')]"
            try:
                click(xpath_next)
            except:
                sleep(1)
                click(xpath_next)

        # --- 取数据
        rows = finds('//div[@class="fs-table__body-wrapper"]/table/tbody/tr')
        for tr in rows:
            items = []
            cells = findchildren(tr,'.//td')
            for i in cellrange:
                items.append(cells[i].text)

            # 流程调度列表中点击 单据号
            if cells[5].text == flowtype:
            
                cells[6].click()
                switchtowindow(1)

                # --- 获取表单值 ---
                # 获得 流程定义名称
                # items.append(find("//span[@class='form-title']").text)
                # print(find("//span[@class='form-title']").text)

                # 获得 流程进度
                items.append(find("//div[@class='process-preview']").text.replace('\n', '； '))

                # 获得 附件
                items.append(find('//div[@class="file-list clearfix"]').text.replace('\n', '； '))

                # 获得 表单值
                j = 0

                for formcomp in finds('//input | //textarea'):
                    j = j + 1
                    if j > len(flowheads):
                        break
                    items.append(formcomp.get_attribute('value').replace('\n', '； '))

                # print(items)

                # 关闭并返回列表
                driver.close()
                switchtowindow(0)
                switchtoframe('iframepage')
                switchtoframe(find('//*[@id="content"]/iframe'))

                # 数据写入文件
                export_writer.writerow(items)

# ----- DONE -----
print('DONE')

driver.close()

# findchildren(find('//div[@class="fs-table__body-wrapper"]/table/tbody/tr'),'.//td')[6].click()
# switchtowindow(1)
# driver.close()
# switchtowindow(0)

# s  = '发起审批\n2018-10-17 10:00\nBD\nBD\n同意\n2018-10-17 10:00\n同一审批人自动审批\n驳回制单\n2018-10-23 09:18\n请用尚敏申请，谢谢。'
# print(s.replace('\n',' | '))