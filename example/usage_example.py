#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import time

from pyspin.spin import make_spin, Spin1


@make_spin(Spin1, "Downloading...")
def demo():
    time.sleep(5)


if __name__ == '__main__':
    print("Assume we're downloading a video")
    print("It would cost much time.")
    demo()
    print("Download success!")
