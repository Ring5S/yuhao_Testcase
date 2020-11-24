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
#
loading_id = 'com.joowing.nebula.online:id/center'
account_login_id = "com.joowing.nebula.online:id/account_login"
login_phone_id = 'com.joowing.nebula.online:id/phone'
# 客服按钮
iv_helper_id = 'com.joowing.nebula.online:id/iv_helper_icon'
account_login_json = {
    'account_name': 'js1@haoshijie.com',
    'account_password': 'js1109'
}
phone_login_json = {
    'phone': '12020102902',
    'org_code': 'jwbaby'
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


driver = appium_start()
driver.implicitly_wait(20)
Slider = Slide(driver)


# 通过id元素进行点击操作
def choose_id_click(ele_id):
    try:
        login_driver = driver.find_element_by_id(ele_id)
        # print(login_driver)
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
    # driver.find_element_by_xpath("//*[@text='今日门店销售']").click()
    # time.sleep(3)
    # driver.back()
    # text_insure = driver.find_elements_by_class_name('android.widget.TextView')
    # a = 1
    # for i in text_insure:
    #     if i.text == '今日门店销售':
    #         print('管理员登录页面显示正常')
    #     if i.text.isdigit():
    #         # 这个地方写的很锉，先这样，后面会根据元素子集关系来定位......
    #         if int(i.text) >= 0:
    #             print(f"一级面板数据{a}层数据显示为{i.text}正常！")
    #         else:
    #             print(f"一级面板数据{a}层数据显示为{i.text}异常！")
    #         a += 1


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


def guider_logon():
    phone_login(phone_login_json)
    time.sleep(3)
    tl = driver.find_elements_by_class_name('android.widget.TextView')
    tl[2].click()
    QR_code_sl = 'text("专属顾问二维码").className("android.widget.TextView")'
    QR_code = driver.find_element_by_android_uiautomator(QR_code_sl)
    QR_code.click()
    ImageView = driver.find_elements_by_class_name('android.widget.ImageView')
    if len(ImageView) != 0:
        time.sleep(3)
        print("专属顾问二维码渲染正常！")
    else:
        time.sleep(6)
        print("专属顾问二维码渲染异常！")
    QR_close = driver.find_elements_by_class_name('android.widget. ')[2]
    QR_close.click()
    time.sleep(2)
    for i in range(4):
        Slider.swipeLeft()
        time.sleep(0.5)
    Slider.swipeDown()
    time.sleep(1)


def show_sales():
    time.sleep(3)
    # 先定位一层数据的子元素，之后找今日门店销售的父元素，再通过该父元素定位父元素，再通过该元素定位数据部分的父元素。。。
    desc_xpath = '//*[@class="android.widget.TextView"][@text="元"]'
    # print(driver.find_element_by_xpath(
    #     '//*[@class="android.widget.TextView"][@text="截至到数据更新时间，今日门店POS累计销售额（不包含服务类）"]').text)
    # 定位到一层元素的第一个子元素，对应一级页面一层右半边的元素
    desc_xpath_fa = f'{desc_xpath}/..'
    # 一层元素
    desc_grand = f'{desc_xpath_fa}/..'
    # 销售面板数据总元素
    top2_grand = f'{desc_grand}/..'
    top2_grand_list = f'{top2_grand}/android.widget.LinearLayout'
    tt = driver.find_elements_by_xpath(top2_grand_list)
    print(tt, len(tt))
    # 当前层的总元素进行遍历
    for i in range(1, len(tt) + 1):
        a = 1
        fa_now = f'{top2_grand_list}[{i}]'
        # 当前层左半边
        fa_left = f'{fa_now}/android.widget.LinearLayout[1]'
        # 当前层左半边标题
        fa_left_title = f'{fa_left}/android.widget.LinearLayout'
        # 标题描述
        left_title = f'{fa_left_title}/android.widget.TextView'
        # 当前层右半边
        fa_right = f'{fa_now}/android.widget.LinearLayout[2]'
        right_data = f'{fa_right}/android.widget.TextView[1]'
        right_desc = f'{fa_right}/android.widget.TextView[2]'
        # 层标题
        title = driver.find_element_by_xpath(left_title).text
        # 层数据
        data = driver.find_element_by_xpath(right_data).text
        if data.isdigit():
            a += 1
        else:
            print(f'{title}数据{data}展示异常')
        # 层数据描述
        desc = driver.find_element_by_xpath(right_desc).text
        print(f'{title}{data}{desc}')


account_login(account_login_json)
show_sales()
# show_sales_data()
# guider_logon()
