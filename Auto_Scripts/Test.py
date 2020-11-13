import time
import json

def time_array():
    a1 = "2019-5-10 23:40:00"
    # 先转换为时间数组
    timeArray = time.strptime(a1, "%Y-%m-%d %H:%M:%S")
    print(timeArray)
    # 转换为时间戳
    timeStamp = int(time.mktime(timeArray))
    print(timeStamp)

    # 格式转换 - 转为 /
    a2 = "2019/5/10 23:40:00"
    # 先转换为时间数组,然后转换为其他格式
    timeArray = time.strptime(a2, "%Y/%m/%d %H:%M:%S")
    otherStyleTime = time.strftime("%Y/%m/%d %H:%M:%S", timeArray)
    print(otherStyleTime)
    return 1, 2, 'a'


# a = time_array()
# print(type(a))
# print(a)
#
# import requests

list1=[0,1,1,1,2,2,3,3]
list=list(set(list1))
print(list)
print(set(list1))