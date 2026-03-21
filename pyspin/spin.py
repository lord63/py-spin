#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import sys
import threading
import time
from functools import wraps
from concurrent.futures import ThreadPoolExecutor

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


def _is_tty(output):
    return getattr(output, 'isatty', lambda: False)()


class Spinner(object):
    def __init__(self, frames=Default, words="", ending="\n"):
        self.frames = frames
        self.length = len(frames)
        self.position = 0
        self.words = words
        self.ending = ending
        self._stop_event = None
        self.spin_thread = None

    def current(self):
        return self.frames[self.position]

    def next(self):
        current_frame = self.current()
        self.position = (self.position + 1) % self.length
        return text_type(current_frame)

    def reset(self):
        self.position = 0

    def _start(self):
        if _is_tty(sys.stdout):
            self._stop_event = threading.Event()
            self.spin_thread = threading.Thread(target=self._init_spin)
            self.spin_thread.start()

    def _stop(self):
        if self.spin_thread:
            self._stop_event.set()
            self.spin_thread.join()
            self.spin_thread = None
            self._stop_event = None

    def _init_spin(self):
        while not self._stop_event.is_set():
            self._spin_cursor()
            time.sleep(0.1)

    def _spin_cursor(self):
        print(text_type("\r{0}    {1}").format(self.next(), self.words), end="")
        sys.stdout.flush()

    def __enter__(self):
        if self.spin_thread and self.spin_thread.is_alive():
            raise RuntimeError("Spinner is already running")
        self._start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        should_print_ending = self.spin_thread is not None
        self._stop()
        if should_print_ending:
            print(self.ending, end="")
            sys.stdout.flush()
        return False


def make_spin(spin_style=Default, words="", ending="\n"):
    spinner = Spinner(spin_style, words, ending)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(func, *args, **kwargs)
                is_tty = _is_tty(sys.stdout)

                if is_tty:
                    while future.running():
                        spinner._spin_cursor()
                        time.sleep(0.1)

                if is_tty:
                    print(spinner.ending, end="")
                return future.result()

        return wrapper

    return decorator
