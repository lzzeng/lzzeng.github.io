---
title: Python题记-04
date: 2021-12-03 22:20:40
tags:
    - Python
categories:
    - Python
copyright:
toc: true
---





> 数字链表，随机密码

<!-- more -->



> 题1：用链表存0-9的数字，然后从头到尾输出其代表的10进制数值（前面的0忽略）
>
> 题2：随机生成8字符的密码
> ```
> 包含1个特殊字符：!#$%&()+,-./:;<=>?@[]^_{}~
> 包含1到2个数字
> 包含大写字母
> 包含小写字母
> 
> 示例：
> 4mOhNkV?
> $pDz0Q9F
> fXi?AGC9
> ```



## 数字链表

```python
# coding=utf8

""" 数字链表
用链表存0-9的数字，然后从头到尾输出其代表的10进制数值（前面的0忽略）

示例：
0 0 1 2 3
输出
123

1 0 3 4 5
输出
10345
"""


class Node(object):
    def __init__(self, v=None):
        self.value = v
        self.next = None

    def __repr__(self):
        return str(self.value)


class Nodes(object):
    def __init__(self, node=None):
        self.head = node

    def get_tail(self):
        cur_node = self.head
        while cur_node.next:
            cur_node = cur_node.next
        return cur_node

    def add_node(self, node):
        if self.head is None:
            self.head = node
        else:
            cur_node = self.get_tail()
            cur_node.next = node

    def print_num(self):
        s = None
        cur_node = self.head
        while cur_node:
            if s is None:
                if cur_node.value:
                    s = str(cur_node.value)
            else:
                s += str(cur_node.value)
            cur_node = cur_node.next
            
        print s


if __name__ == '__main__':
    nums = [0, 0, 5, 6, 7]
    nodes = Nodes()
    for n in nums:
        nodes.add_node(Node(n))

    nodes.print_num()
```



或者Nodes稍作修改

```
class Nodes(object):
    def __init__(self, node=None):
        self.head = node
        self.tail = node

    def add_node(self, node):
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node            
...
```





## 随机密码

```python
# coding=utf8
from random import randint, choice, shuffle
from string import letters, digits, uppercase, lowercase

""" 生成10个随机8位数密码
包含1个特殊字符：!#$%&()+,-./:;<=>?@[]^_{}~
包含1到2个数字
包含大写字母
包含小写字母

示例：
4mOhNkV?
$pDz0Q9F
fXi?AGC9
"""


def create_psw():
    r_lst = []
    my_punctuation = """!#$%&()+,-./:;<=>?@[]^_{}~"""
    r_lst.append(choice(my_punctuation))
    for j in range(randint(1, 2)):
        r_lst.append(choice(digits))
    r_lst.append(choice(uppercase))
    r_lst.append(choice(lowercase))
    for j in range(8 - len(r_lst)):
        r_lst.append(choice(letters + digits))

    shuffle(r_lst)
    return "".join(r_lst)


if __name__ == '__main__':
    for i in range(10):
        print create_psw()
```

