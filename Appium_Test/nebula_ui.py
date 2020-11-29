import time
from appium.webdriver.common.touch_action import TouchAction
from appium import webdriver
from Appium_Test.mainfunction import Slide, BasicMethods
from Auto_Scripts.公共方法 import Login
from Appium_Test.UI流程方法 import BusProcess
from Appium_Test import global_varibals

Login = Login(headers=global_varibals.headers, data=global_varibals.data)
"""
Activity是Android系统中的四大组件之一，可以用于显示View
我们的智零售启动appActivity在Appium调试的时候发现必须得用通过APK包解出来的【launchable-activity】,其他页面启动会报错
配置如下：
caps["appActivity"] = "com.joowing.app.activity.MainActivity" 
"""
#
loading_id = 'com.joowing.nebula.online:id/center'
account_login_id = "com.joowing.nebula.online:id/account_login"
login_phone_id = 'com.joowing.nebula.online:id/phone'
# 客服按钮
iv_helper_id = 'com.joowing.nebula.online:id/iv_helper_icon'
account_login_json = {
    'account_name': global_varibals.account_name,
    'account_password': global_varibals.account_password
}
phone_login_json = {
    'phone': global_varibals.phone,
    'org_code': global_varibals.org_code
}


# 前置代码：Appium启动参数
def appium_start():
    caps = {}
    caps["platformName"] = "Android"
    caps["platformVersion"] = "10"
    caps["deviceName"] = "Redmi_K20_Pro_Premium_Edition"
    caps["appPackage"] = "com.joowing.nebula.online"
    caps["appActivity"] = "com.joowing.app.activity.MainActivity"
    # caps["noReset"] 为False时，每次调试app时会默认重置app状态为对应acctivity入口，为True则按照打开调试app时app的当前入口来操作
    caps["noReset"] = False
    caps["ensureWebviewsHavePages"] = True
    # 一定要开启Appium的服务
    driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps)
    return driver


# 准备实例化
driver = appium_start()
driver.implicitly_wait(20)
Slider = Slide(driver)
BusProcess = BusProcess(driver)
BasicMethods = BasicMethods(driver)


# 账号密码登录
def account_login(info):
    choose_id_click = BasicMethods.choose_id_click(account_login_id)
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


# 手机号获取验证码登录
def phone_login(phone_login_info):
    user_captcha = ""
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


# -----------------------------后台管理员账户登录以及UI验证流程-------------------------
def administrators_ui():
    account_login(account_login_json)
    # 下拉刷新下数据
    Slider.swipeDown()
    c1 = BusProcess.show_sales()
    if c1:
        print('管理员一级面板数据展示正常！')
    else:
        print("检测管理员一级面板数据展示异常！")
    Slider.swipeLeft()
    Slider.swipeUp()
    c2 = BusProcess.show_sales()
    if c2:
        print('店长一级面板数据展示正常！')
        if c1:
            print("--------------一级面板数据验证完毕--------------------")
    else:
        print("检测店长一级面板数据展示异常！")
    Slider.swipeRight()


# ------------------------------导购手机号登录以及UI验证流程---------------------------
def guider_ui():
    phone_login(phone_login_json)
    BusProcess.guider_login()


# noinspection PyBroadException
try:
    administrators_ui()
    BusProcess.secondary_panel()
    BusProcess.third_panel()
except Exception as e:
    print("--------------一级面板UI验证异常！见异常截图-------------------")
    driver = appium_start()
    driver.implicitly_wait(20)
    Slider = Slide(driver)
    administrators_ui()
    BusProcess.secondary_panel()
    BusProcess.third_panel()
