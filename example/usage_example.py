#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import time

from pyspin import spin
from pyspin.spin import make_spin


@make_spin(spin.Spin1, "Downloading...")
def demo():
    print("Assume we're downloading a video")
    print("It would cost much time.")
    time.sleep(5)
    print("Download success!")


if __name__ == '__main__':
    demo()
