#!/usr/bin/env python

import sys
import threading
import time
from functools import wraps
from concurrent.futures import ThreadPoolExecutor

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

# isatty is not part of any formal interface, so guard against streams that
# define it as a non-callable attribute (e.g. a plain bool) rather than a method.
def _is_tty(output):
    isatty_attr = getattr(output, 'isatty', None)
    if callable(isatty_attr):
        return isatty_attr()
    if isinstance(isatty_attr, bool):
        return isatty_attr
    return False


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
        return str(current_frame)

    def reset(self):
        self.position = 0

    def _start(self):
        if _is_tty(sys.stdout):
            self._stop_event = threading.Event()
            # daemon=True: if the process exits unexpectedly without calling
            # _stop(), this thread is killed automatically instead of keeping
            # the process alive.
            self.spin_thread = threading.Thread(
                target=self._init_spin,
                daemon=True,
                name="SpinnerThread",
            )
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

    def _spin_cursor(self):
        print("\r{0}    {1}".format(self.next(), self.words), end="")
        sys.stdout.flush()
        time.sleep(0.1)

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
            # The ending may not contain a newline, so flush explicitly to
            # ensure it appears on screen before the caller continues.
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
                    # Use done() rather than running(): a future sits in PENDING
                    # state briefly after submit() where running() is False, which
                    # would cause the loop to exit before the task even starts.
                    while not future.done():
                        spinner._spin_cursor()

                if is_tty:
                    print(spinner.ending, end="")
                    sys.stdout.flush()
                return future.result()

        return wrapper

    return decorator
