import time
from appium.webdriver.common.touch_action import TouchAction
from appium import webdriver
from Appium_Test.mainfunction import Slide
from Auto_Scripts.公共方法 import Login

# 部分场景需要用到接口部分查询
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
    'Connection': 'keep-alive'
}
data = {}
Login = Login(headers=headers, data=data)
"""
Activity是Android系统中的四大组件之一，可以用于显示View
我们的智零售启动appActivity在Appium调试的时候发现必须得用通过APK包解出来的【launchable-activity】,其他页面启动会报错
配置如下：
caps["appActivity"] = "com.joowing.app.activity.MainActivity" 
"""
# 前置代码：Appium启动参数
caps = {}
caps["platformName"] = "Android"
caps["platformVersion"] = "10"
caps["deviceName"] = "Redmi_K20_Pro_Premium_Edition"
caps["appPackage"] = "com.joowing.nebula.online"
caps["appActivity"] = "com.joowing.app.activity.MainActivity"
# caps["noReset"] 为False时，每次调试app时会默认重置app状态为对应acctivity入口，为True则按照打开调试app时app的当前入口来操作
caps["noReset"] = False
caps["ensureWebviewsHavePages"] = True
driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps)
driver.implicitly_wait(20)

account_login_id = "com.joowing.nebula.online:id/account_login"
login_phone_id = 'com.joowing.nebula.online:id/phone'
account_login_json = {
    'account_name': 'js1@jwbaby.com',
    'account_password': 'js1109'
}
phone_login_json = {
    'phone': '12020102902',
    'org_code': 'jwbaby'
}
Slider = Slide(driver)


# 通过id元素进行点击操作
def choose_id_click(ele_id):
    try:
        login_driver = driver.find_element_by_id(ele_id)
        print(login_driver)
        login_driver.click()
        time.sleep(0.6)
    except Exception as e:
        if e:
            print('ID定位异常，请检查后重试！')
            exit()


# 账号密码登录
def account_login(info):
    choose_id_click(account_login_id)
    # 模拟登录智零售后通过账号密码登录的操作，由于我的手机进入账号密码登录页面后会自动跳出可选择的账号，会影响元素定位，所以随便点个地方取消账号选择
    TouchAction(driver).tap(x=646, y=1119).perform()
    name = info['account_name']
    password = info['account_password']
    test1 = driver.find_elements_by_id("com.joowing.nebula.online:id/user_name")
    # print(test1, test1[0].text)
    test1[0].send_keys(name)
    time.sleep(1)
    TouchAction(driver).tap(x=646, y=1119).perform()
    driver.find_elements_by_id("com.joowing.nebula.online:id/password")[0].send_keys(password)
    login_button_id = 'com.joowing.nebula.online:id/login_button'
    driver.find_elements_by_id(login_button_id)[0].click()
    time.sleep(8)
    TouchAction(driver).tap(x=745, y=160).perform()
    text_insure = driver.find_elements_by_class_name('android.widget.TextView')
    for i in text_insure:
        num = text_insure.index(i)
        if i.text == '今日门店销售':
            print('管理员登录页面显示正常')
        if i.text.isdigit():
            # 这个地方写的很锉，先这样，后面会根据元素位置来定位......
            if int(i.text) >= 0:
                print(f"一级面板数据第{num}层正常！")
            else:
                print("一级面板销售数据异常！")


# 手机号获取验证码登录
def phone_login(phone_login_info):
    org_code = phone_login_info['org_code']
    phone = phone_login_info['phone']
    phone_index = str(phone)[-4:]
    driver.find_element_by_id(login_phone_id).send_keys(phone)
    driver.find_element_by_id('com.joowing.nebula.online:id/captchaButton').click()
    index_url = f'http://jmp.joowing.com/api/ris/global/user_captcha/all_captcha?org_code={org_code}&phone_index={phone_index}'
    Jmp_Seeion = Login.JMP_Login()
    time.sleep(5)
    user_captcha_list = Jmp_Seeion.get(index_url).json()
    # print(Jmp_Seeion.get(index_url).json())
    if len(user_captcha_list) == 0:
        print('未查询到手机号！请确认手机号是否唯一')
        exit()
    else:
        user_captcha = user_captcha_list[0]['captcha']
    driver.find_element_by_id('com.joowing.nebula.online:id/captcha').send_keys(user_captcha)
    driver.find_element_by_id('com.joowing.nebula.online:id/login_button').click()


#   面板数据点击展示
def show_sales_data():
    # 组合定位，一般组合用id,class,text这三个属性会比较好一点
    # id+class 属性组合
    id_class = 'text("今日门店销售").className("android.widget.TextView")'
    text = driver.find_element_by_android_uiautomator(id_class)
    time.sleep(4)
    # 向上滑动智零售面板
    Slider.swipeUp()
    time.sleep(6)
    sl = driver.find_elements_by_class_name('android.widget.Button')
    sl[0].click()


account_login(account_login_json)
# phone_login(phone_login_json)
show_sales_data()
