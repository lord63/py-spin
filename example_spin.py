#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import sys
import time

import spin


def show(name, frames):
    s = spin.Spinner(frames)
    print(name)
    for i in range(30):
        time.sleep(0.1)
        print("\r{0}".format(s.next()), end="")
        sys.stdout.flush()
    print('\n')


def main():
    show("Default", spin.Default)
    show("Box1", spin.Box1)
    show("Box2", spin.Box2)
    show("Box3", spin.Box3)
    show("Box4", spin.Box4)
    show("Box5", spin.Box5)
    show("Box6", spin.Box6)
    show("Box7", spin.Box7)
    show("Spin1", spin.Spin1)
    show("Spin2", spin.Spin2)
    show("Spin3", spin.Spin3)
    show("Spin4", spin.Spin4)
    show("Spin5", spin.Spin5)
    show("Spin6", spin.Spin6)
    show("Spin7", spin.Spin7)
    show("Spin8", spin.Spin8)
    show("Spin9", spin.Spin9)


if __name__ == '__main__':
    main()
