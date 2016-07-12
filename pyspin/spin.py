#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import sys
import time
from functools import wraps
from multiprocessing import Process, Queue


# For python 2/3 compatible.
if sys.version_info.major == 2:
    text_type = unicode
else:
    text_type = str


Box1 = u'⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
Box2 = u'⠋⠙⠚⠞⠖⠦⠴⠲⠳⠓'
Box3 = u'⠄⠆⠇⠋⠙⠸⠰⠠⠰⠸⠙⠋⠇⠆'
Box4 = u'⠋⠙⠚⠒⠂⠂⠒⠲⠴⠦⠖⠒⠐⠐⠒⠓⠋'
Box5 = u'⠁⠉⠙⠚⠒⠂⠂⠒⠲⠴⠤⠄⠄⠤⠴⠲⠒⠂⠂⠒⠚⠙⠉⠁'
Box6 = u'⠈⠉⠋⠓⠒⠐⠐⠒⠖⠦⠤⠠⠠⠤⠦⠖⠒⠐⠐⠒⠓⠋⠉⠈'
Box7 = u'⠁⠁⠉⠙⠚⠒⠂⠂⠒⠲⠴⠤⠄⠄⠤⠠⠠⠤⠦⠖⠒⠐⠐⠒⠓⠋⠉⠈⠈'
Spin1 = u'|/-\\'
Spin2 = u'◴◷◶◵'
Spin3 = u'◰◳◲◱'
Spin4 = u'◐◓◑◒'
Spin5 = u'▉▊▋▌▍▎▏▎▍▌▋▊▉'
Spin6 = u'▌▄▐▀'
Spin7 = u'╫╪'
Spin8 = u'■□▪▫'
Spin9 = u'←↑→↓'
Default = Box1


class Spinner(object):
    def __init__(self, frames):
        self.frames = frames
        self.length = len(frames)
        self.position = 0

    def current(self):
        return self.frames[self.position]

    def next(self):
        current_frame = self.current()
        self.position = (self.position + 1) % self.length
        return text_type(current_frame)

    def reset(self):
        self.position = 0


def make_spin(spin_style=Default, words=""):
    spinner = Spinner(spin_style)
    queue = Queue()

    def add_queue(func):
        @wraps(func)
        def wrapper():
            func()
            queue.put_nowait(1)
        return wrapper

    def decorator(func):
        @wraps(func)
        def wrapper():
            process = Process(target=add_queue(func))
            process.start()
            while queue.empty():
                print(text_type("\r{0}    {1}").format(spinner.next(), words),
                      end="")
                sys.stdout.flush()
                time.sleep(0.1)
            queue.get()
            print('')
        return wrapper
    return decorator
