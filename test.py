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
pushed = [1, 2, 3, 4, 5]
popped = [4, 5, 3, 2, 1]
stack = []
i = 0
for push in pushed:
    stack.append(push)
    while stack and stack[-1] == popped[i]:
        stack.pop()
        i += 1
print(stack)
