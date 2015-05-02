#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import sys
import time


Box1 = '⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
Box2 = '⠋⠙⠚⠞⠖⠦⠴⠲⠳⠓'
Box3 = '⠄⠆⠇⠋⠙⠸⠰⠠⠰⠸⠙⠋⠇⠆'
Box4 = '⠋⠙⠚⠒⠂⠂⠒⠲⠴⠦⠖⠒⠐⠐⠒⠓⠋'
Box5 = '⠁⠉⠙⠚⠒⠂⠂⠒⠲⠴⠤⠄⠄⠤⠴⠲⠒⠂⠂⠒⠚⠙⠉⠁'
Box6 = '⠈⠉⠋⠓⠒⠐⠐⠒⠖⠦⠤⠠⠠⠤⠦⠖⠒⠐⠐⠒⠓⠋⠉⠈'
Box7 = '⠁⠁⠉⠙⠚⠒⠂⠂⠒⠲⠴⠤⠄⠄⠤⠠⠠⠤⠦⠖⠒⠐⠐⠒⠓⠋⠉⠈⠈'
Spin1 = '|/-\\'
Spin2 = '◴◷◶◵'
Spin3 = '◰◳◲◱'
Spin4 = '◐◓◑◒'
Spin5 = '▉▊▋▌▍▎▏▎▍▌▋▊▉'
Spin6 = '▌▄▐▀'
Spin7 = '╫╪'
Spin8 = '■□▪▫'
Spin9 = '←↑→↓'
Default = Box1


class Spinner(object):
    def __init__(self, frames):
        self.frames = frames
        self.length = len(frames)
        self.position = 0

    def current(self):
        return self.frames[self.position]

    def next(self):
        if self.position == self.length - 1:
            self.reset()
        else:
            self.position = self.position + 1
        return self.frames[self.position]

    def reset(self):
        self.position = 0

    def animate(self, words='', interval=0.1):
        while(self.position != -1):
            print("\r{0}    {1}".format(self.next(), words), end="")
            time.sleep(interval)
            sys.stdout.flush()
        print("\n")

    def stop(self):
        self.position = -1
