#!/usr/bin/env python3

##################
# OMIS 自动化测试脚本
##################

from selenium import webdriver
import time

driver = webdriver.Chrome('/Users/mxj/Downloads/chromedriver')
# driver.fullscreen_window()



#====== 定义快捷方法 ========

# 定义 点击 方法
def click(xpath, delay=.5):
    driver.find_element_by_xpath(xpath).click()
    time.sleep(delay)

# 定义 展开子菜单 方法
def navopen(menutitle, delay=.5):
    menu = driver.find_element_by_xpath("//div[@class='el-submenu__title']//span[contains(text(),'" + menutitle + "')]")
    if "is-opened" not in menu.find_element_by_xpath("./../..").get_attribute("class"):
        menu.click() 
        time.sleep(delay)

# 定义 点击菜单 方法
def navto(menutitle):
    click("//li[contains(@class,'el-menu-item')]//span[contains(text(),'" + menutitle + "')]")


# 定义 点击全局操作按钮 方法
def navclick(text):
    click("//div[@class='leftList']//span[contains(text(),'" + text + "')]")


# 定义 输入字符 方法
def sendkeys(xpath, keys, delay=.5):
    driver.find_element_by_xpath(xpath).send_keys(keys)
    time.sleep(delay)

# 定义 通过标签文字获取表单中的输入框 方法
def getforminput(label,index = 0):
    return driver.find_elements_by_xpath("//form//label[contains(text(),'" + label +"')]/following-sibling::div//input")[index]

# 定义 表单输入文字 方法
def formfill(label, value, index = 0, isAppend=False):
    input = getforminput(label, index)
    # TODO ISSUE: 在 邮编 中 clear() 无效
    if not isAppend:
        input.clear()
    input.send_keys(value)

# 定义 表单下拉选择 方法
def formselect(label, option, index = 0):
    getforminput(label, index).click()
    time.sleep(.5)
    driver.find_element_by_xpath("//li[contains(@class,'el-select-dropdown__item')]//span[contains(text(),'" + option + "')]").click()
    time.sleep(.5)



# ====== 访问网站 =====
driver.get('http://xxxxxxxxxx/MyOMS/')
time.sleep(3)


#====== 系统登入 ======
if driver.find_element_by_xpath("//form[@id='loginForm']"):
    sendkeys("//input[@id='userID']","xxxx")
    sendkeys("//input[@id='password']","xxxxx\n")

    click("//input[@placeholder='请选择登录门店']")
    click("//span[contains(text(),'000203.家家公寓')]")

    click("//button[@id='login-btn']")


#====== 测试企业档案 ======
navopen("档案管理")
navopen("租户档案")
navto("企业档案管理")

navclick("新增企业档案")

formselect("企业类型","有限合伙")
formfill("企业英文","ibm")
formselect("国家","比利时")
formfill("邮编","200002",1,True)

# 返回
navclick("返回")

