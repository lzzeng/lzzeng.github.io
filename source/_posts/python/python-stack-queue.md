---
title: Python模拟栈和队列
date: 2020-09-17 16:30:00
tags:    
    - Python
categories:
    - Python

copyright: true
---



```sh
How to reduce 'attention residue' in your life 
 34 Many of us struggle with the never-ending nature of our to-do lists, says Elizabeth Emens, author of The Art of Life Admin and a New York-based professor     of law at Columbia University.
```



<!-- more -->



模拟栈随机存取若干字符：

```sh
[root@VM_0_13_centos pyQueueStack]# python stack.py 

+6: H o w   t o 
-5: o t   w o 
+5:   r e d u 
-7: u d e r   H (empty) 
+5: c e   ' a 
+4: t t e n 
+6: t i o n   r 
-6: r   n o i t 
+7: e s i d u e ' 
-6: ' e u d i s 
-5: e n e t t 
+3:   i n 
+4:   y o u 
-7: u o y   n i   
-3: a '   
-5: e c (empty) 
+5: r   l i f 
+4: e ? 
-4: ? e f i 
-3: l   r 
End.
```



模拟队列随机存取若干字符：

```sh
[root@VM_0_13_centos pyQueueStack]# python queue.py 

+7: H o w   t o   
+7: r e d u c e   
+4: ' a t t 
+3: e n t 
+7: i o n   r e s 
+7: i d u e '   i 
+3: n   y 
+3: o u r 
+4:   l i f 
+5: e ? 
-5: H o w   t 
-6: o   r e d u 
-7: c e   ' a t t 
-3: e n t 
-5: i o n   r 
-6: e s i d u e 
-7: '   i n   y o 
-6: u r   l i f 
-7: e ? (empty) 
End.
```



模拟 2个栈 实现 队列：

```sh
[root@VM_0_13_centos pyQueueStack]# python stack2queue.py 

+4: H o w   
+7: t o   r e d u 
+3: c e   
+4: ' a t t 
+5: e n t i o 
+4: n   r e 
+4: s i d u 
+5: e '   i n 
+5:   y o u r 
+6:   l i f e ? 
-3: H o w 
-4:   t o   
-6: r e d u c e 
-4:   ' a t 
-6: t e n t i o 
-7: n   r e s i d 
-7: u e '   i n   
-7: y o u r   l i 
-4: f e ? (empty) 
End.
```



```python
# coding=utf-8

import random


class SequenceStack(object):
    def __init__(self):
        self.__members = list()

    def is_empty(self):
        return not len(self.__members)

    def push(self, data):
        self.__members.append(data)

    def pop(self):
        if self.is_empty():
            return
        return self.__members.pop()
        
    def length(self):
        return len(self.__members)

    def check(self):
        if self.is_empty():
            return
        return self.__members[-1]


class Queue(object):
    def __init__(self):
        self.__stackA = SequenceStack()
        self.__stackB = SequenceStack()
    
    def is_empty(self):
         return self.__stackA.is_empty() and self.__stackB.is_empty()

    def offer(self, e):
        self.__stackA.push(e)

    def poll(self):
        if self.__stackB.is_empty():
            while not self.__stackA.is_empty():
                self.__stackB.push(self.__stackA.pop())
        return self.__stackB.pop()


if __name__ == '__main__':
    q = Queue()
    s = """How to reduce 'attention residue' in your life?"""
    n_pos = 0
    while True:
        # is_offer = int(random.random()*2) == 1 and n_pos < len(s)
        is_offer = n_pos < len(s)
        in_num = int(random.random()*5) + 3
        out_num = int(random.random()*5) + 3
        if is_offer:
            print "\n+%1d:" % in_num,
            for e in s[n_pos:n_pos+in_num]:
                print e,
                q.offer(e)
            n_pos += in_num
        else:
            print "\n-%1d:" % out_num,
            for i in range(out_num):
                if q.is_empty():
                    print "(empty)",
                    break
                print q.poll(),
            if q.is_empty() and n_pos >= len(s):
                break

    print "\nEnd."
```



队列 当 栈 使用：

```sh
[root@VM_0_13_centos pyQueueStack]# python queue2stack.py 

+3: H o w 
+5:   t o   r 
+7: e d u c e   ' 
+5: a t t e n 
+4: t i o n 
+6:   r e s i d 
+4: u e '   
-7:   ' e u d i s 
+3: i n   
+7: y o u r   l i 
+7: f e ? 
-5: ? e f i l 
-5:   r u o y 
-6:   n i e r   
-5: n o i t n 
-3: e t t 
-3: a '   
-7: e c u d e r   
-6: o t   w o H 
End.
```



[附件：stack.py](/assets/files/stack-queue/stack.py)

[附件：queue.py](/assets/files/stack-queue/queue.py)

[附件：stack2queue.py](/assets/files/stack-queue/stack2queue.py)

[附件：queue2stack.py](/assets/files/stack-queue/queue2stack.py)

