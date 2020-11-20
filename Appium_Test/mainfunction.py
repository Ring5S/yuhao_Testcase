class Slide:

    def __init__(self, driver):
        self.driver = driver

    def get_screen_size(self):
        x = self.driver.get_window_size()['width']  # 获取屏幕宽度
        y = self.driver.get_window_size()['height']  # 获取屏幕高度
        return (x, y)

    def swipeLeft(self):
        l = self.get_screen_size()
        x1 = int(l[0] * 0.75)
        y1 = int(l[1] * 0.5)
        x2 = int(l[0] * 0.25)
        self.driver.swipe(x1, y1, x2, y1)
        print('向左滑动')

    def swipeRight(self):
        l = self.get_screen_size()
        x1 = int(l[0] * 0.25)
        y1 = int(l[1] * 0.5)
        x2 = int(l[0] * 0.75)
        self.driver.swipe(x1, y1, x2, y1)
        print('向右滑动')

    def swipeUp(self):
        l = self.get_screen_size()
        x1 = int(l[0] * 0.5)
        y1 = int(l[1] * 0.75)
        y2 = int(l[1] * 0.25)
        self.driver.swipe(x1, y1, x1, y2, 3)
        print('向上滑动')

    def swipeDown(self):
        l = self.get_screen_size()
        x1 = int(l[0] * 0.5)
        y1 = int(l[1] * 0.25)
        y2 = int(l[1] * 0.75)
        self.driver.swipe(x1, y1, x1, y2)
        print('向下滑动')


if __name__ == '__main__':
    """
    #三种appium设置等待时间的方法
    #参考了网上的资料，然后进行了梳理
    
    #第一种 sleep()： 设置固定休眠时间。 python 的 time 包提供了休眠方法 sleep() ， 导入 time包后就可以使用 sleep()进行脚本的执行过程进行休眠。
    #导入 time 包
    import time
    time.sleep()
    
    #第二种 implicitly_wait()：是 webdirver 提供的一个超时等待。隐的等待一个元素被发现，或一个命令完成。如果超出了设置时间的则抛出异常。
    #implicitly_wait():隐式等待
    #当使用了隐式等待执行测试的时候，如果 WebDriver没有在 DOM中找到元素，将继续等待，超出设定时间后则抛出找不到元素的异常
    #换句话说，当查找元素或元素并没有立即出现的时候，隐式等待将等待一段时间再查找 DOM，默认的时间是0
    #一旦设置了隐式等待，则它存在整个 WebDriver 对象实例的声明周期中，隐式的等到会让一个正常响应的应用的测试变慢，
    #它将会在寻找每个元素的时候都进行等待，这样会增加整个测试执行的时间。
    
    #implicitly_wait()方法比 sleep() 更加智能，后者只能选择一个固定的时间的等待，前者可以在一个时间
    #范围内智能的等待。
    self.driver.implicitly_wait()
    
    #第三种  WebDriverWait()：同样也是 webdirver 提供的方法。在设置时间内，默认每隔一段时间检测一次当前。页面元素是否存在，如果超过设置时间检测不到则抛出异常。
    '''详细格式如下：
    WebDriverWait(driver, timeout, poll_frequency=0.5, ignored_exceptions=None)
    driver - WebDriver 的驱动程序(Ie, Firefox, Chrome 或远程)
    timeout - 最长超时时间，默认以秒为单位
    poll_frequency - 休眠时间的间隔（步长）时间，默认为 0.5 秒
    ignored_exceptions - 超时后的异常信息，默认情况下抛 NoSuchElementException 异常。
    WebDriverWait()一般由 until()或 until_not()方法配合使用，下面是 until()和 until_not()方法的说明。
    until(method, message=’’)
    调用该方法提供的驱动程序作为一个参数，直到返回值不为 False。
    until_not(method, message=’’)
    调用该方法提供的驱动程序作为一个参数，直到返回值为 False。
    lambda
    lambda 提供了一个运行时动态创建函数的方法。'''
    
    from selenium.webdriver.support.ui import WebDriverWait
    element = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id(“someId”))
    is_disappeared = WebDriverWait(driver, 30, 1, (ElementNotVisibleException)).
    until_not(lambda x: x.find_element_by_id(“someId”).is_displayed())
    """
