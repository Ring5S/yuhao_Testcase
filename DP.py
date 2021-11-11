# 人生第一个独立DP
t = "ahbgdc"  # x 对应里面的小表
s = "abc"  # y 对应外层大表
s = list(s)
t = list(t)
s.insert(0, "")
t.insert(0, "")
leny = len(s)
lenx = len(t)
dp = []
for y in range(leny):
    si = []
    for x in range(lenx):
        si.append(0 * x)
    dp.append(si)
print(dp)
dp[0][0] = True
for y in range(leny):
    for x in range(lenx):
        if x == y == 0:
            continue
        if x > 0 and t[x] != s[y]:
            dp[y][x] = dp[y][x - 1]
        elif x > 0 and t[x] == s[y]:
            dp[y][x] = dp[y - 1][x - 1]
        else:
            dp[y][x] = False
print(dp)
