def lengthOfLongestSubstring(s):
#   筛选字串
    li = []
    len_s = len(s)
    # if len_s > 100:
    #     return 1
    for o in range(len_s):
        for i in range(1, len_s + 1):
            if o > i:
                continue
            else:
                if len(s[o:i]) > 0:
                    li.append(s[o:i])
                else:
                    continue
            # print(s[o:i])
    if len(li) > 200:
        li = ["a"]
    return li


def huiwen(s):
#   判断回文
    res = True
    if len(s) % 2 == 0:
        for i in range(int(len(s) / 2)):
            # print(s[i], s[-1 - i])
            if s[i] == s[-1 - i]:
                pass
            else:
                res = False
                break
    else:
        mid = int(len(s) / 2) + 1
        # print("mid", mid)
        for i in range(mid):
            # print(s[i], s[-1 - i])
            if i == mid:
                continue
            if s[i] == s[-1 - i]:
                pass
            else:
                res = False
                break
    return res
# DP构造
s1 = "abcde"
s2 = "ace"
s1_list = list(s1)
s2_list = list(s2)
s1_list.insert(0, "")
s2_list.insert(0, "")

len1 = len(s1_list)
len2 = len(s2_list)
print(len1, len2)
dp = []
# 构造一个DP表，row行cel列
for row in range(len2):
    cel_l = []
    for cel in range(len1):
        cel_l.append(cel)
    dp.append(cel_l)
# print(dp)
dp[0][0] = 0

# 经典栈
class Solution:
    def validateStackSequences(self, pushed, popped) -> bool:
        stack = []
        for i in range(len(pushed)):
            stack.append(pushed[i])
            while stack[-1] == popped[0]:
                print(stack)
                popped.pop(0)
                stack.pop(-1)
                print(stack)
                if len(stack) == 0:
                    break
        print(stack)
        return not stack
    
# 思路：将多维度复合排序整合成单一列简单排序


def func(in_list):
    nation = []
    for word in in_total.strip().split('\n'):
        nation.append(word.strip().split())
    return nation

#将字母也转换成按顺序排位的小数
def letter_num(string):
    string = string.lower()
    s = '0abcdefghijklmnopqrstuvwxyz'
    result = ''
    for i in range(0,len(string)):
        result = result +str(100 - s.index(string[i]))
    return result

if __name__ == "__main__":
    in_total = ''
    #一次性输入多行
    country_num = 0
    n = 9999999999
    while country_num <= n:
        strs = input()
        if country_num == 0:
            n = int(strs)
            country_num += 1
        else:
            in_total += strs
            in_total += '\n'
            country_num += 1
#取的input数组
    list_input = func(in_total)
    result = []
#获取排名
    for i in list_input:
        result.append((i[0],float(str(int(i[1])*1000000 + int(i[2])*1000 + int(i[3])) + '.' +letter_num(i[0]))))
    result =  sorted(result, key=lambda result : result[1],reverse=True)
#输出
    output = ''
    for i in result:
        output += i[0] + '\n'
    print(output)
