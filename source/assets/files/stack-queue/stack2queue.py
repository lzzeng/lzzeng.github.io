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
    s2 = """How to reduce 'attention residue' in your life 
Many of us struggle with the never-ending nature of our to-do lists, says Elizabeth Emens, author of The Art of Life Admin and a New York-based professor of law at Columbia University."""
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

