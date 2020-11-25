import time


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
        y1 = int(l[1] * 0.8)
        y2 = int(l[1] * 0.25)
        self.driver.swipe(x1, y1, x1, y2)
        print('向上滑动')

    def swipeDown(self):
        l = self.get_screen_size()
        x1 = int(l[0] * 0.5)
        y1 = int(l[1] * 0.2)
        y2 = int(l[1] * 0.75)
        self.driver.swipe(x1, y1, x1, y2)
        print('向下滑动')


class BasicMethods:
    def __init__(self, driver):
        self.driver = driver

    # 通过id元素进行点击操作
    def choose_id_click(self, eld_id):
        driver = self.driver
        try:
            ele_driver = driver.find_element_by_id(eld_id)
            ele_driver.click()
            time.sleep(0.6)
        except Exception as e:
            if e:
                print(e)
                print('ID定位异常，请检查后重试！')
                exit()


if __name__ == '__main__':
    pass
