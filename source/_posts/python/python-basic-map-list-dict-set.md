---
title: Python Basic 01
date: 2020-10-07 16:30:00
tags:    
    - Python
categories:
    - Python

copyright: 
toc: true
---



> 列表和字典类型 —— 这可能是在Python程序中所见到并使用的两种最常见、最具有灵活性而且功能最为强大的集合体类型。



<!-- more -->



## map 映射

map()是Python内置的高阶函数，它接收一个函数 f 和一个 list，并通过把函数 f 依次作用在 list 的每个元素上，得到一个新的 list 并返回。

```sh
>>> L = map(str, [1, 2, 4])         # int转str
>>> L2 = list(L)
>>> for e in L:                     # L 已经迭代过了，不会print
...   print(e)
... 
>>>
>>> L2
['1', '2', '4']

>>> L = list(map(ord, 'abcd'))              # ord 字符转ASC-II码
>>> L
[97, 98, 99, 100]

>>> L = list(map(chr, range(97,100)))       # chr ASC-II码转字符
>>> L
['a', 'b', 'c']

>>> list(map(str.upper, ['a', 'B', 'c']))   # 转大写
['A', 'B', 'C']

>>> d2
{'b': '555', 'c': [3, 4, 5], 'a': {'aa': [9, 11], 'bb': 44}, (1, 2, 6): '999'}
>>> list(map(str, d2))                      # 提取keys，并转化为str了
['b', 'c', 'a', '(1, 2, 6)']
```



## list 有序集

### remove方法按给定元素删除

```sh
>>> a = ['a', 'b', 'a', 2, 3, 2]
>>> a
['a', 'b', 'a', 2, 3, 2]
>>> a.remove('a')
>>> a
['b', 'a', 2, 3, 2]
>>> a.remove(2)
>>> a
['b', 'a', 3, 2]    # remove删除的是左边第一个找到的元素
```

### pop方法按index删除

```sh
>>> a = ['a', 'b', 'a', 2, 3, 2]
>>> a.pop(2)
'a'
>>> a
['a', 'b', 2, 3, 2]

>>> a = ['a', 'b', 'a', 2, 3, 2]
>>> a.pop()                         # 不给定index时，pop的是末尾元素，等同于 a.pop(-1)
2
>>> a
['a', 'b', 'a', 2, 3]
```

### del命令也可以删除列表元素，按index删除

```sh
>>> a = ['a', 'b', 'a', 2, 3, 2]
>>> del a[2]
>>> a
['a', 'b', 2, 3, 2]

>>> del a         # del列表名 会删除此列表
>>> a
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'a' is not defined
```



### 列表分片赋值

分片赋值最好分成两步来理解：

> 1.删除, 删除等号左边指定的分片, 含头不含尾。
>
> 2.插入, 将包含在等号右边对象中的片段插入旧分片被删除的位置。

```sh
>>> L = [1, 3, 5, 7, 9]
>>> L
[1, 3, 5, 7, 9]
>>> L[1:3] = [2, 4, 6, 8]
>>> L
[1, 2, 4, 6, 8, 7, 9]
>>> 
>>> L[1:5] = []                 # 分片赋值[] 相当于删除分片元素
>>> L
[1, 7, 9]

>>> L[1:3] = [2, 4, 6, 8]
>>> L
[1, 2, 4, 6, 8]
>>> del L[1:3]                  # del命令删除分片
>>> L
[1, 6, 8]

>>> L2
['A', 'a', 'b', 'C']
>>> L2[:] = []                  # [:]分片表示全部元素，此处删除全部元素
>>> L2
[]

>>> L2
['A', 'a', 'b', 'C']
>>> del L2[:]
>>> L2
[]
>>> del L2
>>> L2
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'L2' is not defined
```

### sort

```sh
>>> L = ['a', 'A', 'b', 'C']
>>> L.sort()
>>> L
['A', 'C', 'a', 'b']
>>> L.sort(reverse=True)
>>> L
['b', 'a', 'C', 'A']

>>> L
['A', 'C', 'a', 'b']
>>> L.sort(key=str.lower)           # ？统一按小写排序，小写后相同的保留原顺序
>>> L
['A', 'a', 'b', 'C']

# L.sort(key=str.upper) 与 L.sort(key=str.lower) 效果相同
```



## set 无序集

```sh
>>> a = set(1,2,3)                    # set和list 不能通过参数列表的方式初始化元素
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: set expected at most 1 arguments, got 3
>>> 
>>> a = set([1,2,3])                  # 方式一：转化list为set
>>> a
{1, 2, 3}
>>> a = {1,2,3,4}                     # 方式二：使用{}
>>> a
{1, 2, 3, 4}
>>> a.pop(3)                          # 因无序，没有pop(index)方法，del命令也是
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: pop() takes no arguments (1 given)
>>> a.remove(3)                       # 有remove(element)方法，按元素删除；不要混淆pop，没有pop(element)方法
>>> a
{1, 2, 4}
>>> a = {1,2,2,3}                     # 初始元素含重复，会自动剔除重复元素
>>> a
{1, 2, 3}
```



## dict 字典

Python 3.0中的keys返回一个迭代器，在Python 2.6中，keys构建并返回一个真正的列表


### 初始化

```sh
>>> d = {'a': 1, 'b': 2, 'c': [3,4,5]}      # 方式一
>>> d = dict(a=1, b=2, c=[3,4,5])           # 方式二

>>> d = {}                                  # 方式三，逐行赋值法
>>> d['a'] = 1
>>> d['b'] = 2
>>> d['c'] = [3,4,5]

>>> d4 = dict.fromkeys(['a', 'b', 'c'], 0)  # 方式四，此方法只能指定key，参数二是公共的值，不写则为None
>>> d4
{'a': 0, 'b': 0, 'c': 0}
>>> d4 = dict.fromkeys(['a', 'b', 'c'])
>>> d4
{'a': None, 'b': None, 'c': None}

>>> D3 = dict.fromkeys('abcd')                    # 四-2, 注意'dict'字符串被分割，如同 for e in 'abcd'
>>> D3
{'a': None, 'b': None, 'c': None, 'd': None}

>>> D2 = {k:v for k,v  in zip(['a','b','c'], [1,2,3])}     # 解析法
>>> D2
{'a': 1, 'b': 2, 'c': 3}

>>> # 其它转化法
```

### 2个list通过zip合并成dict

```sh
>>> list_a = ['a', 'b', 'c']
>>> list_b = [1, 2, [3,4,5]]
>>> zip(list_a,list_b)
<zip object at 0x7f8d0b714e08>
>>> list(zip(list_a,list_b))
[('a', 1), ('b', 2), ('c', [3, 4, 5])]
>>> dict(zip(list_a, list_b))
{'a': 1, 'b': 2, 'c': [3, 4, 5]}

>>> a = zip(list_a, list_b)                 # zip 迭代器类型
>>> type(a)
<class 'zip'>
>>> for m,n in a:
...     print(f'{m},{n}')
... 
a,1
b,2
c,[3, 4, 5]
```

### items

```sh
>>> d = {'a': 1, 'b': 2, 'c': [3,4,5]}
>>> d
{'a': 1, 'b': 2, 'c': [3, 4, 5]}
>>> d.items
<built-in method items of dict object at 0x7f8d0b7924c8>
>>> d.items()
dict_items([('a', 1), ('b', 2), ('c', [3, 4, 5])])      # d.items() 是dict_items类型
>>> items = list(d.items())
>>> items
[('a', 1), ('b', 2), ('c', [3, 4, 5])]

>>> for k,v in d.items():
...     print(f"{k}:{v}")
... 
a:1
b:2
c:[3, 4, 5]
```

### dict是可变类型

```sh
>>> d
{'a': 1, 'b': 2, 'c': [3, 4, 5]}
>>> 
>>> d2 = d
>>> d is d2
True
>>> 
>>> d['a'] = 1.1
>>> d
{'a': 1.1, 'b': 2, 'c': [3, 4, 5]}
>>> d2
{'a': 1.1, 'b': 2, 'c': [3, 4, 5]}

>>> d.pop('a')                          # dict 有pop(key)方法，相当于get(key)并del d[key]
1.1
>>> d
{'b': 2, 'c': [3, 4, 5]}

>>> d.remove('a')                       # ! dict 没有remove或delete方法
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'dict' object has no attribute 'remove'
>>> d.delete('a')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'dict' object has no attribute 'delete'

>>> del d['a']                          # del 命令可以按key删除
>>> d
{'b': 2, 'c': [3, 4, 5]}
```



## copy和deepcopy

### copy

字典、列表本身有copy方法

> 拷贝需要注意的是：无条件值的分片以及字典copy方法只能做顶层复制。也就是说，不能够复制嵌套的数据结构（如果有的话）。如果你需要一个深层嵌套的数据结构的完整的、完全独立的拷贝，那么就要使用标准的copy模块——包括import copy语句，并编辑X = copy.deepcopy（Y）对任意嵌套对象Y做完整的复制。

- 没有限制条件的分片表达式(L[:])能够复制序列。
- 字典copy方法(X.copy())能够复制字典。
- 有些内置函数, 例如list, 能够生成拷贝(list(L))。
- copy标准库模块能够生成完整拷贝。


```sh
>>> d
{'b': 2, 'c': [3, 4, 5], 'a': {'aa': [8, 9], 'bb': 22}}
>>> d2 = d
>>> d2
{'b': 2, 'c': [3, 4, 5], 'a': {'aa': [8, 9], 'bb': 22}}
>>> d3 = d.copy()
>>> d3['a'] = 'abc'
>>> d3
{'b': 2, 'c': [3, 4, 5], 'a': 'abc'}
>>> d
{'b': 2, 'c': [3, 4, 5], 'a': {'aa': [8, 9], 'bb': 22}}
>>> 

>>> d['b'] = 222
>>> d2
{'b': 222, 'c': [3, 4, 5], 'a': {'aa': [8, 9], 'bb': 22}}
>>> d
{'b': 222, 'c': [3, 4, 5], 'a': {'aa': [8, 9], 'bb': 22}}
>>> d3
{'b': 2, 'c': [3, 4, 5], 'a': 'abc'}


>>> L = [1,3,5,7]
>>> L2 = L
>>> L3 = L.copy()             # L3是对L的独立的复制
>>> L3
[1, 3, 5, 7]
>>> L3[1] = 2                 # L3改变 L和L2不变
>>> L3
[1, 2, 5, 7]
>>> L
[1, 3, 5, 7]
>>> L2
[1, 3, 5, 7]

>>> L[1] = 100                # L改变，L2跟着变，L3不变
>>> L
[1, 100, 5, 7]
>>> L2
[1, 100, 5, 7]
>>> L3
[1, 2, 5, 7]

>>> L4 = L[:]                 # [:]分片相当于L.copy(), L[0:], L[0:4]也一样
>>> L4
[1, 100, 5, 7]
>>> L4[1] = 99
>>> L4
[1, 99, 5, 7]
>>> L
[1, 100, 5, 7]
>>> L2
[1, 100, 5, 7]
>>> L3
[1, 2, 5, 7]
```

### deepcopy

copy只复制顶层结构, deepcopy可以复制嵌套的数据结构

```sh
>>> d
{'b': 222, 'c': [3, 4, 5], 'a': {'aa': [8, 9], 'bb': 22}}
>>> 
>>> d2 = d.copy()
>>> d2
{'b': 222, 'c': [3, 4, 5], 'a': {'aa': [8, 9], 'bb': 22}}
>>> d['a']['aa'] = [8, 9, 10]                                   # 修改第二层数据，会发现d2 仍然随 d 变化，因为对key:'a'的value复制的是引用
>>> d
{'b': 222, 'c': [3, 4, 5], 'a': {'aa': [8, 9, 10], 'bb': 22}}
>>> d2 
{'b': 222, 'c': [3, 4, 5], 'a': {'aa': [8, 9, 10], 'bb': 22}}
>>> 
>>> d['b'] = 333                                                # 修改顶层数据则不会
>>> d
{'b': 333, 'c': [3, 4, 5], 'a': {'aa': [8, 9, 10], 'bb': 22}}
>>> d2
{'b': 222, 'c': [3, 4, 5], 'a': {'aa': [8, 9, 10], 'bb': 22}}

>>> import copy
>>> d3 = copy.deepcopy(d)                                       # deepcopy可以实现嵌套引用结构的复制
>>> d3
{'b': 333, 'c': [3, 4, 5], 'a': {'aa': [8, 9, 10], 'bb': 22}}
>>> d['a']['aa'] = [9, 11]
>>> d
{'b': 333, 'c': [3, 4, 5], 'a': {'aa': [9, 11], 'bb': 22}}
>>> d3
{'b': 333, 'c': [3, 4, 5], 'a': {'aa': [8, 9, 10], 'bb': 22}}   # 没变
>>> d2
{'b': 222, 'c': [3, 4, 5], 'a': {'aa': [9, 11], 'bb': 22}}
```

进一步测试

```sh
>>> d2
{'b': '222', 'c': [3, 4, 5], 'a': {'aa': [9, 11], 'bb': 22}}
>>> d4 = d2.copy()
>>> d4 is d2
False
>>> d4 == d2
True
>>> d2['b'] is d4['b']                # 使用copy时，对于不可变对象和（嵌套的）可变对象，都是复制（顶层）地址
True                                  # 因此，当顶层不可变对象修改时，互不影响
>>> d2['b'] = '555'
>>> d4['b']
222
>>> d2['b'] is d4['b']
False
>>> 
>>> d2['a']['bb'] = 44                # 而嵌套结构修改时，因为是原地修改（顶层地址不变），原始对象和复制对象一起改变
>>> d2
{'b': '555', 'c': [3, 4, 5], 'a': {'aa': [9, 11], 'bb': 44}}
>>> d4
{'b': 222, 'c': [3, 4, 5], 'a': {'aa': [9, 11], 'bb': 44}}
>>> d2['a']['bb'] is d4['a']['bb']    # 虽然子层 d2['a']['bb'] 是int不可变类型修改时第二层的相应地址变了
True                                  # ，但因为所关联的顶层地址不变，所以复制对象与原始对象保持一致
                                      # copy复制的对象 可以看作时 栈内存中的一个内存位置所指向的堆内存的顶层地址列表

>>> d3 = copy.deepcopy(d2)
>>> d3
{'b': '555', 'c': [3, 4, 5], 'a': {'aa': [9, 11], 'bb': 22}}
>>> d3['b'] is d2['b']
True
>>> d3['c'] is d2['c']
False
>>> d3['c'][0] is d2['c'][0]
True
>>> d3['a'] is d2['a']
False
>>> d3['a']['bb'] is d2['a']['bb']
True
>>> d3['a']['aa'] is d2['a']['aa']
False
>>> d3['a']['aa'][0] is d2['a']['aa'][0]
True
```



## 比较大小

一般来说，Python中不同的类型的比较方法如下：
- 数字通过相对大小进行比较。
- 字符串是按照字典顺序，一个字符接一个字符地对比进行比较（"abc" < "ac"）。
- 列表和元组从左到右对每部分的内容进行比较。
- 字典通过排序之后的（键、值）列表进行比较。字典的相对大小比较在Python 3.0中不支持

```sh
>>> d
{'b': 333, 'c': [3, 4, 5], 'a': {'aa': [8, 9, 10], 'bb': 22}}
>>> d2
{'b': 222, 'c': [3, 4, 5], 'a': {'aa': [8, 9, 10], 'bb': 22}}
>>> 
>>> d3 = d
>>> d3 is d
True
>>> d4 = d2.copy()
>>> d4 is d2
False
>>> d4 == d2                  # 可以测试是否相等 ==
True
>>> d2 < d                    # 但 python3 中不支持比大小 > <
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: '<' not supported between instances of 'dict' and 'dict'
```
