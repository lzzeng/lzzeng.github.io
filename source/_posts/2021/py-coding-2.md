---
title: python编程（二）
date: 2021-10-27 23:55:40
tags:
    - Python
categories:
    - Python
copyright:
toc: true
---





## 求质因子

> 题目：输入一个正整数，按照从小到大的顺序输出它的所有质因子（重复的也要列举，如180的质因子为2 2 3 3 5 ）

<!-- more -->



递归拆解：
```python
"""
以180为例，因子列表会依次变化如下：
[180]
[2, 90]
[2, 2, 45]
[2, 2, 3, 15]
[2, 2, 3, 3, 5]  # 不可继续拆解了，此时就是质因子列表
"""

def f(x):
    for k in range(x, len(a)):
        v = a[k]
        flag = False
        for i in xrange(2, int(v ** 0.5 + 1)):
            if v % i == 0:
                flag = True
                a.pop(k)
                a.append(i)
                v /= i
                if v > 1:
                    a.append(v)
                break

        if flag:
            f(k + 1)
        else:
            break

m = int(raw_input())
a = [m]
f(0)
for i in a:
    print i,
```



特别解法：
```python
"""
能被2，3，5 ... 整除则print，接着以【商】递归。注意break的位置！
"""

def prime(a):
    mark = 1
    for i in range(2, int(a ** 0.5 + 2)):
        if a % i == 0:
            mark = 0
            print i,
            b = int(a / i)
            prime(b)
            break
    if mark == 1:
        print a,

prime(int(input()))
```



用循环替代递归：
```python
from __future__ import print_function
import math

def get_result(num):
    end = int(math.sqrt(num))
    for i in xrange(2, end+1):
        while num % i == 0:
            print(i, end=" ")
            num /= i
            flag = True
    if num != 1:
        print(num, end=" ")

a = raw_input()
get_result(int(a))
```





## 动态规划

> 题目：购物单问题
>
> 如果要买归类为附件的物品，必须先买该附件所属的主件；
> 每个主件可以有 0 个、 1 个或 2 个附件；
> 附件不再有从属于自己的附件；
> 每件物品规定了一个重要度，分为 5 等：用整数 1 **~** 5 表示，第 5 等最重要；
> 每件物品的价格都是10元的整数倍；
> 希望在不超过 N 元（可以等于 N 元）的前提下，使每件物品的价格与重要度的乘积的总和最大。
> 求这个最大值。



参考解法：
```python
"""
示例输入：
1000 5
800 2 0
400 5 1
300 5 1
400 3 0
500 2 0

输出：
2200

说明：
1000 5 中1000是总预算，5表示下面列出5件候选商品
接下的第一行：800 2 0 表示第一件是主件（0），重要度2，价格800
第二行：400 5 1 表示第二件是附件（非0），且是第一件（1）的附件，重要度5，价格400
以下类推
"""


n, m = map(int, raw_input().split())
pri, anex = {}, {}
for i in range(1, m + 1):
    v, p, q = map(int, raw_input().split())
    if q == 0:
        pri[i] = [v, p]
    else:
        if q in anex:
            anex[q].append([v, p])
        else:
            anex[q] = [[v, p]]
            
dp = [0] * (n + 1)
for key in pri:  # 对于每一个主件
    w, v = [], []  # 计算 该主件+附件 各种组合的w,v
    w.append(pri[key][0])  # 仅主件
    v.append(pri[key][0] * pri[key][1])
    if key in anex:
        w.append(w[0] + anex[key][0][0])  # 主件+附件1 的价格
        v.append(v[0] + anex[key][0][0] * anex[key][0][1])
        if len(anex[key]) >= 2:
            w.append(w[0] + anex[key][1][0])  # 主件+附件2
            v.append(v[0] + anex[key][1][0] * anex[key][1][1])
            w.append(w[0] + anex[key][0][0] + anex[key][1][0])  # 主件+附件1+附件2
            v.append(v[0] + anex[key][0][0] * anex[key][0][1] + anex[key][1][0] * anex[key][1][1])
            
    for j in range(n, -1, -10):
        for k in range(len(w)):
            # 如果够买第k组合，当前金额dp 和 剩余金额dp+本组合v 大者更新为当前dp
            if j - w[k] >= 0:
                dp[j] = max(dp[j], dp[j - w[k]] + v[k])
                
print dp[n]
```





## 走方格

> 题目：计算n*m的棋盘格子（n为横向的格子数，m为竖向的格子数，m<=8）从棋盘左上角出发沿着边缘线从左上角走到右下角，总共有多少种走法，要求不能走回头路，即：只能往右和往下走，不能往左和往上走。
>
> 注：沿棋盘格之间的边缘线行走



递归法：
```python
def p_mn(m, n):
    if m == 1 or n == 1:
        return m + n
    return p_mn(m - 1, n) + p_mn(m, n - 1)

m, n = map(int, raw_input().split())
if m > 8:
    break
print p_mn(m, n)
```



公式法（阶乘）：
```python
from math import factorial as f

try:
    while 1:
        n, m = map(int, raw_input().split())
        print f(n + m) / (f(m) * f(n))
except:
    pass
```



如果不知道从math导入，可自定义阶乘函数：
```python
def factorial(n):
    ans = 1
    while n:
        ans *= n
        n -= 1
    return ans
```

如何证明可以按这个公式？看起来像是排列组合或概率统计的问题。
f(n+m)是既不考虑顺序，又不考虑方向的排列数，f(m)和f(n)分别是竖向、横向不考虑顺序的排列数。
