from selenium import webdriver
import time

"""打开NB并登录"""
driver = webdriver.Chrome()
driver.get('http://nb3.joowing.com/nebula/security/sign-in')
time.sleep(2)
driver.find_element_by_xpath('//*[@id="input_0"]').click()
driver.maximize_window()
driver.find_element_by_xpath('//*[@id="input_0"]').send_keys('js1@demo.com')
driver.find_element_by_xpath('//*[@id="input_1"]').send_keys('js1109')
driver.find_element_by_xpath('//*[@id="sign-in-form"]/form/button/span').click()
time.sleep(3)
driver.find_element_by_xpath('//*[@id="vertical-navigation"]/div/div[1]/div/ul/li[2]/span').click()
time.sleep(2)
driver.find_element_by_xpath('//*[@id="vertical-navigation"]/div/div[1]/div/ul/li[5]/span').click()
yxgl_xpath = '//*[@id="vertical-navigation"]/div/div[2]/ms-navigation/ul/li[5]/div/div/span'
quick_scheme = '//*[@id="vertical-navigation"]/div/div[2]/ms-navigation/ul/li[5]/ul/li[1]/div/a/span'
time.sleep(1)
driver.find_element_by_xpath(yxgl_xpath).click()
time.sleep(3)
driver.find_element_by_xpath(quick_scheme).click()

driver.quit()
