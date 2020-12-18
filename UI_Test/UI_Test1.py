class aa:
    def __init__(self):
        pass

    def action1(self):
        a = 100
        global a
        try:
            print(1)
        except Exception as e:
            print(e)

    def action2(self):
        try:
            print("哈哈哈哈哈哈")
            self.action1()
        except Exception as e:
            print(e)
        print(a)


aa().action1()
