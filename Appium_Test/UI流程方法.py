import time
from Appium_Test.mainfunction import Slide
from appium.webdriver.common.touch_action import TouchAction


class BusProcess:
    def __init__(self, driver):
        self.driver = driver

    # 判断字符串是否为数字
    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
        return False

    def guider_login(self):
        driver = self.driver
        Slider = Slide(driver)
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
        QR_close = driver.find_elements_by_class_name('android.widget.TextView')[2]
        QR_close.click()
        time.sleep(2)
        for i in range(4):
            Slider.swipeLeft()
            time.sleep(0.5)
        Slider.swipeDown()
        time.sleep(1)

    def show_sales(self):
        # 一级面板数据验证的思路：先通过父子和相邻层级关系，遍历面板数据，并对每层的数据进行数字分析并计数，通过最终计数来判定是否全部成功.
        driver = self.driver
        time.sleep(0.8)
        # 先定位一层数据的子元素，之后找今日门店销售的父元素，再通过该父元素定位父元素，再通过该元素定位数据部分的父元素。。。
        desc_xpath = '//*[@class="android.widget.TextView"][@text="元"]'
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
        a = 1
        for i in range(1, len(tt) + 1):
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
            is_number = self.is_number(data)
            # 判断一级面板展示的数据是否为数字并且大于等于0，才可通过
            if is_number and float(data) >= 0:
                a += 1
            else:
                print(f'{title}数据{data}展示异常')
            # 层数据描述
            desc = driver.find_element_by_xpath(right_desc).text
            print(f'{title}{data}{desc}')
        if a == len(tt) + 1:
            return True
        else:
            return False

    # 通过点击一级面板数据进入二级面板
    def secondary_panel(self):
        driver = self.driver
        Slider = Slide(driver)
        desc_xpath = '//*[@class="android.widget.TextView"][@text="元"]'
        t = driver.find_element_by_xpath(desc_xpath)
        t.click()
        time.sleep(0.6)
        # 进入二级面板后，对四个分类板块进行遍历点击下拉操作
        sale_xpath = '//*[@class="android.widget.Button"][@content-desc="销售数据"]'
        # driver.find_element_by_xpath(sale_xpath)
        # 销售数据父层
        sale_xpath_fa = f'{sale_xpath}/..'
        # a1 = driver.find_elements_by_xpath(f'{sale_xpath_fa}/android.widget.Button')
        # print(len(a1))
        # 销售数据按钮
        sale_xpath_fa3 = f'{sale_xpath_fa}/android.widget.Button[3]'
        # 门店详情按钮
        sale_xpath_fa4 = f'{sale_xpath_fa}/android.widget.Button[4]'
        # 品类详情按钮
        sale_xpath_fa5 = f'{sale_xpath_fa}/android.widget.Button[5]'
        # 品类会员按钮
        sale_xpath_fa6 = f'{sale_xpath_fa}/android.widget.Button[6]'
        for i in range(3, 7):
            time.sleep(1)
            t = driver.find_element_by_xpath(f'{sale_xpath_fa}/android.widget.Button[{i}]')
            t.click()
            time.sleep(0.5)
            Slider.swipeUp()
            Slider.swipeDown()
            time.sleep(0.3)
        print("-------------二级面板UI验证完成，即将跳转三级页面-----------------")
        time.sleep(1)
        t = driver.find_element_by_xpath(sale_xpath_fa3)
        t.click()
        # 通过点击二级面板数据进入三级面板

    def third_panel(self):
        driver = self.driver
        third_xpath = '//*[@class="android.view.View"][@content-desc="点击查看: 明星实收导购>>>更多"]'
        third_l = driver.find_element_by_xpath(third_xpath)
        third_l.click()
