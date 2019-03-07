from selenium import webdriver
import time

dr = webdriver.Chrome('/Users/mxj/Downloads/chromedriver')
# dr.fullscreen_window()
# dr.get('https://www.baidu.com')
dr.get('http://101.132.107.121/MyOMS/')
dr.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div/div/div').click()
time.sleep(0.1)
dr.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/ul/li[1]').click()
dr.find_element_by_xpath('//*[@id="userID"]').send_keys('admin\n123456\n')

classStr = dr.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div/div[1]/div/ul/li[2]').get_attribute('class')
print(classStr)
if 'is-opened' not in classStr:
    dr.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div/div[1]/div/ul/li[2]/div').click()
time.sleep(0.1)
dr.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div/div[1]/div/ul/li[2]/ul/li[1]').click()
# dr.back()
# dr.find_element_by_id('kw').send_keys('selenium\n')

# time.sleep(5)

# dr.close()
