---
title: HJ-01
date: 2021-08-25 23:55:40
tags:
    - Python
categories:
    - Python
copyright:
toc: true
---





## 字符串

### 分割、逆序

字符逆序

```python
""" 字符串反转 数字颠倒 字符逆序 """

print raw_input()[::-1]
```

<!-- more -->



单词逆序

```python
""" 单词逆序
i am a student

student a am i
"""

# S1:
import re
line = raw_input()
a = re.findall("[A-Za-z]+", line)
print ' '.join(a[::-1])

# S2:
print " ".join(reversed(raw_input().split()))

# S3:
print " ".join(raw_input().split()[::-1])
```



字符串最后一个单词的长度

```python
""" 字符串最后一个单词的长度
hello abc

3
"""

s = raw_input()
lst = s.split(' ')
print(len(lst[-1]))
```



字符串分割

```python
""" 字符串分割 每8个字符分割 不足则右补零
abc
123456789

abc00000
12345678
90000000
"""

while True:
    try:
        s = raw_input()
        while len(s) > 8:
            print s[:8]
            s = s[8:]
        print s.ljust(8, "0")
    except:
        break
```



### 字符数

统计不重复的字符总数

```python
""" 统计不重复的字符总数
abc

3
"""

s = raw_input()
sn = set()
for c in s:
    sn.add(c)

print(len(sn))


# 其实一行就够了
print(len(set(s)))
```



统计各字符的数量

```python
""" 统计各字符的数量
hello

{'h': 1, 'e': 1, 'l': 2, 'o': 1}
"""

s = raw_input()
d = dict(zip(s, [0] * len(s)))
for c in s:
    d[c] += 1
print d
```



### 回文

```python
""" 最长的对称部分 最长回文长度问题
ADEFFFFFFFFF

9
"""
```



**正向查找法：**先假定边界 再比较长度

```python
s = raw_input()
nmax = 1
j = len(s)

while True:
    if j <= nmax:
        break
    j -= 1
    for k in xrange(0, j):
        ss = s[k:j + 1]
        if ss == ss[::-1]:
            if j - k + 1 > nmax:
                nmax = j - k + 1

print nmax
```



**逆向查找法：**先假定最大长度，再查找是否存在这样的子字符串

```python
def f(s):
    for length in range(len(s), -1, -1):
        for index in range(0, len(s) - length + 1):
            sub_string = s[index:length + index]
            if sub_string == sub_string[::-1]:
                return len(sub_string)

a = input()
if a:
    print(f(a))
```



**单层循环法**：最快

```python
s = raw_input()
m = 0
for i in range(len(s)):
    if i - m >= 1 and s[i - m - 1:i + 1] == s[i - m - 1:i + 1][::-1]:
        m += 2
    elif i - m >= 0 and s[i - m:i + 1] == s[i - m:i + 1][::-1]:
        m += 1
        
print m
```



## 字典、列表

合并表记录

```python
""" 合并表记录
3
0 1
0 2
1 2

0 3
1 2
"""

d = {}
n = int(raw_input())
for i in range(n):
    # k, v = [int(e) for e in raw_input().split()]
    k, v = map(int, raw_input().split())
    if k in d:
        d[k] += v
    else:
        d[k] = v

for k, v in d.items():
    print k, v
```



查找兄弟单词

```python
""" 查找兄弟单词
6 cab ad abcd cba abc bca abc 1

3
bca

说明：
abc的兄弟单词有cab cba bca，所以输出3
经字典序排列后，变为bca cab cba，所以第1个字典序兄弟单词为bca
"""

s = raw_input().strip().split()
n = int(s.pop(0))
a, x, k = s[:n], s[n], int(s[-1])
y = sorted(x)
temp = sorted([i for i in a if i != x and sorted(i) == y])
print len(temp)
if k <= len(temp):
    print temp[k - 1]
```



## 数字

### 二进制

```python
""" 十进制数 二进制形式1的个数
7

3
"""

print bin(input()).count("1")

# 注意类型：
print type(input())         # int
print type(raw_input())     # str
```



```python
""" 二进制数问题 最长的连续1的个数 """

# S0:
s = bin(int(raw_input()))[2:]
for i in range(len(s), 0, -1):
    if '1' * i in s:
        print i
        break

        
# S2: 正则法 稍慢一点点
import re

print len(max(re.findall(r'1{1,}', bin(int(raw_input()))[2:]), key=len))
```



### 最小公倍数

```python
a, b = map(int, raw_input().split())
if a == b:
    print a
    exit()

if a > b:
    a, b = b, a

for i in xrange(1, a + 1):
    c = b * i
    if c % a == 0:
        print c
        break
```



**循环求余法：**可同时求出 最小公倍数 和 最大公约数

```python
m, n = map(int, raw_input().split())
p = m * n
t = 0

while n != 0:
    t = m
    m = n
    n = t % n

print p / m  # m 即最大公约数, p/m 即最小公倍数
```



## 生成器

求斐波那契数列第n项

```python
from timeit import default_timer as timer

def g(n):
    """
    有边界，限制n个，就需要根据 n 来判断是否 yield
    :param n:
    :return:
    """
    if n > 0:
        yield 1

    if n > 1:
        yield 1

    if n > 2:
        a, b, i = 1, 1, 2
        while i != n:
            a, b = b, a + b
            yield b
            i += 1

# 或者：
# def g(n):
#     a, b, counter = 1, 1, 0
#     while True:
#         if (counter > n):
#             return
#         yield a
#         a, b = b, a + b
#         counter += 1
            
# def g():
#     """
#     无边界限制
#     :return:
#     """
#     yield 1
#     yield 1
#     a, b = 1, 1
#     while True:
#         a, b = b, a + b
#         yield b

while True:
    try:
        n = int(raw_input())
        tic = timer()
        for i, e in enumerate(g(n), start=1):
            if i == n:
                print e
                break
        toc = timer()
        print toc - tic
    except:
        break
```



累计法：

```python
while True:
    try:
        i = int(raw_input())
        tic = timer()
        a, b = 1, 1
        n = 1
        if i > 2:
            for i in range(3, i + 1):
                n = a + b
                a = b
                b = n
        print n
        toc = timer()
        print toc - tic
    except:
        break
```

