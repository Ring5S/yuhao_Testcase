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
