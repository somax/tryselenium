#!/usr/bin/env python3

from selenium import webdriver
import time
import csv

dr = webdriver.Chrome('/Users/mxj/Downloads/chromedriver')
dr.fullscreen_window()

dr.get('https://ec.yonyoucloud.com/')

#======= 登录 =======
login = dr.find_element_by_link_text('登录')
if login:
    login.click()
    dr.find_element_by_xpath('//*[@id="loginType"]/div[2]').click()
    time.sleep(20)
else:
    print('已经登录')
    time.sleep(1)


#======= 切换空间 =======
# dr.switch_to.window(dr.window_handles[0])
dr.find_element_by_xpath("//span[@class='fs-qz-dropdown-link']").click()
time.sleep(1)
# 永菱 尚敏
dr.find_element_by_xpath('//li/span[contains(text(),"永菱")]').click()

#======= 切换到数据列表 =======
# 点击 审批
dr.find_element_by_xpath('//div[@title="审批"]').click()
time.sleep(3)

# 点击 BPM后台
# dr.switch_to_frame('iframepage')
dr.switch_to.frame('iframepage')
dr.find_element_by_xpath('//span[contains(text(),"BPM后台")]').click()
time.sleep(1)

# 点击 流程调度
dr.switch_to.frame(dr.find_element_by_xpath('//*[@id="content"]/iframe'))
dr.find_element_by_xpath('//span[contains(text(),"流程调度")]').click()
# dr.find_element_by_xpath('//span[contains(text(),"任务调度")]').click()
time.sleep(2)
dr.find_element_by_xpath('//span[contains(text(),"全部")]').click()
time.sleep(2)

#======= 获取数据 =======
with open('export1.csv', mode='w') as export:
    export_writer = csv.writer(export, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # 标题栏
    # header = dr.find_elements_by_xpath('//div[@class="fs-table__header-wrapper"]/table/thead/tr/th')
    headrow = []
    for title in dr.find_elements_by_xpath('//div[@class="fs-table__header-wrapper"]/table/thead/tr/th'):
        headrow.append(title.text)

    export_writer.writerow(headrow)

    # 内容
    content = ''
    # next = dr.find_element_by_xpath('//button[@class="btn-next"]')
    next = dr.find_element_by_xpath('//button[contains(@class,"btn-next")]')
    time.sleep(5)

    isdone = False
    while isdone != True:
        rows = dr.find_elements_by_xpath('//div[@class="fs-table__body-wrapper"]/table/tbody/tr')
        for tr in rows:
            row = []
            for td in tr.find_elements_by_xpath('.//td'):
                row.append(td.text)

            export_writer.writerow(row)

        # next = dr.find_element_by_xpath('//button[contains(@class,"btn-next")]')
        if 'disabled' in next.get_attribute('class'):
            isdone = True
        
        next.click()
        time.sleep(5)

# ----- DONE -----

# 以下为临时测试用
# 流程调度列表中点击 单据号
dr.find_elements_by_xpath('//div[@class="fs-table__body-wrapper"]/table/tbody/tr')[5].find_elements_by_xpath('.//td')[6].click()
dr.switch_to.window(dr.window_handles[1])

# 获取表单值

# 预算内付款
# 付款内容,付款合同号,付款描述,合同总金额,本次付款金额,合同已付金额,收款人名称,开户银行,银行卡账号,制单人

# 获得 流程定义名称
dr.find_element_by_xpath("//span[@class='form-title']").text

# 获得 流程进度
dr.find_element_by_xpath("//div[@class='process-preview']").text

# 获得 附件
dr.find_element_by_xpath('//div[@class="file-list clearfix"]').text

# 获得 表单值
formrows = []
for formcomp in dr.find_elements_by_xpath('//input | //textarea'):
    formrows.append(formcomp.get_attribute('value'))

print(formrows)


