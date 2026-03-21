#!/usr/bin/env python3
# Style showcase — runs each built-in spinner style so you can see what it looks like.

import time

from pyspin import spin

STYLES = [
    ("Default", spin.Default),
    ("Box1",    spin.Box1),
    ("Box2",    spin.Box2),
    ("Box3",    spin.Box3),
    ("Box4",    spin.Box4),
    ("Box5",    spin.Box5),
    ("Box6",    spin.Box6),
    ("Box7",    spin.Box7),
    ("Spin1",   spin.Spin1),
    ("Spin2",   spin.Spin2),
    ("Spin3",   spin.Spin3),
    ("Spin4",   spin.Spin4),
    ("Spin5",   spin.Spin5),
    ("Spin6",   spin.Spin6),
    ("Spin7",   spin.Spin7),
    ("Spin8",   spin.Spin8),
    ("Spin9",   spin.Spin9),
]


def show(name, frames):
    s = spin.Spinner(frames)
    print(name)
    for i in range(50):
        print("\r{0}".format(s.next()), end="", flush=True)
        time.sleep(0.1)
    print('\n')


def main():
    for name, frames in STYLES:
        show(name, frames)


if __name__ == '__main__':
    main()
