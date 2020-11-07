from sshtunnel import SSHTunnelForwarder
import os
import threading
import time
import requests
import tkinter.messagebox
from multiprocessing import pool

orglist = ['nycnyy', 'frjeyy', 'wzyza', 'xtaed', 'alggb', 'yyplmm', 'aqmmbb', 'jnbym', 'zsxtd', 'ptbabyplan',
           'dgaiyibaby', 'hsmmsj', 'gdfbb', 'thmmbb', 'hmaxbb', 'lxayjbb', 'wlbbq', 'shgoldsun', 'wwqinzileyuan',
           'hzcc', 'btymb']

code = "demo"


def action(code):
    org_code = code
    print(f"{org_code}.w.joowing.com;")
    time.sleep(1)


# pool_size = 1
# pool = pool.ThreadPool()  # 创建一个线程池
# pool.map(action, orglist)  # 往线程池中填线程
# pool.close()  # 关闭线程池，不再接受线程
# pool.join()  # 等待线程池中线程全部执行完

import threading


def myTestFunc(name):
    print(f"我是一个函数，名称是{name}")


t = threading.Thread(target=myTestFunc, args="1")  # 创建一个线程
t.start()  # 启动线程
os.listdir("/")