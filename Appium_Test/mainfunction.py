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
        y1 = int(l[1] * 0.3)
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
    pass
