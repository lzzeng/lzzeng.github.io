# coding=utf-8

import random


class Queue(object):
    def __init__(self):
        self.__members = list()

    def is_empty(self):
        return not len(self.__members)

    def offer(self, data):
        self.__members.append(data)

    def poll(self):
        if self.is_empty():
            return
        e0 = self.__members[0]
        del self.__members[0]
        return e0
        
    def length(self):
        return len(self.__members)


class MyStack(object):
    def __init__(self):
        self.__queueA = Queue()
    
    def _is_empty(self):
         return self.__queueA.is_empty()

    def push(self, e):
        self.__queueA.offer(e)

    def pop(self):
        qlen = self.__queueA.length()
        if qlen > 1:
            for i in range(qlen-1):
                self.__queueA.offer(self.__queueA.poll())

        return self.__queueA.poll()

    def length(self):
        return self.__queueA.length()


if __name__ == '__main__':
    q = MyStack()
    s = """How to reduce 'attention residue' in your life?"""
    s2 = """How to reduce 'attention residue' in your life 
Many of us struggle with the never-ending nature of our to-do lists, says Elizabeth Emens, author of The Art of Life Admin and a New York-based professor of law at Columbia University."""
    n_pos = 0
    while True:
        is_push = int(random.random()*2) == 1 and n_pos < len(s)
        # is_push = n_pos < len(s)
        in_num = int(random.random()*5) + 3
        # out_num = int(random.random()*5) + 3
        out_num = min(int(random.random()*5) + 3, q.length())
        if is_push:
            print "\n+%1d:" % in_num,
            for e in s[n_pos:n_pos+in_num]:
                print e,
                q.push(e)
            n_pos += in_num
        else:
            if 0 == out_num:
                continue
            print "\n-%1d:" % out_num,
            for i in range(out_num):
                if q._is_empty():
                    print "(empty)",
                    break
                print q.pop(),
            if q._is_empty() and n_pos >= len(s):
                break

    print "\nEnd."

