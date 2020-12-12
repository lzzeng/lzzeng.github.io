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


if __name__ == '__main__':
    q = SequenceStack()
    s = """How to reduce 'attention residue' in your life?"""
    s2 = """How to reduce 'attention residue' in your life 
Many of us struggle with the never-ending nature of our to-do lists, says Elizabeth Emens, author of The Art of Life Admin and a New York-based professor of law at Columbia University."""
    n_pos = 0
    while True:
        is_push = int(random.random()*2) == 1 and n_pos < len(s)
        # is_push = n_pos < len(s)
        in_num = int(random.random()*5) + 3
        out_num = int(random.random()*5) + 3
        # out_num = min(int(random.random()*5) + 3, q.length())
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
                if q.is_empty():
                    print "(empty)",
                    break
                print q.pop(),
            if q.is_empty() and n_pos >= len(s):
                break

    print "\nEnd."

