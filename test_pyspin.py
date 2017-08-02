#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from pyspin import spin


def test_spinner():
    spinner = spin.Spinner(spin.Spin9)
    assert spinner.length == 4
    assert spinner.frames == spin.Spin9

    assert spinner.current() == u'←'

    assert spinner.next() == u'←'
    assert spinner.next() == u'↑'
    assert spinner.next() == u'→'
    assert spinner.next() == u'↓'
    assert spinner.next() == u'←'
    assert spinner.next() == u'↑'

    spinner.reset()
    assert spinner.position == 0


def test_make_spin():
    @spin.make_spin(spin.Default, 'Downloading...')
    def fake_download():
        time.sleep(2)

    fake_download()


def test_make_spin_with_args():
    @spin.make_spin(spin.Default, 'Downloading...')
    def fake_download(url, retry_times=3):
        print("Downloading {0}, will retry {1} times".format(url, retry_times))
        time.sleep(2)

    fake_download("https://www.example.com/text.txt", retry_times=5)


def test_stop_on_exception():
    @spin.make_spin(spin.Default, 'Downloading...')
    def fake_download():
        1 / 0

    try:
        fake_download()
    except ZeroDivisionError:
        print("We catched the exception! Yeah!")


def test_several_calls():
    @spin.make_spin(spin.Default, 'Downloading...')
    def fake_download():
        time.sleep(2)

    print("Begin the first download.")
    fake_download()
    print("Begin the second download.")
    fake_download()


def test_context_manager():
    def fake_download():
        time.sleep(2)

    with spin.Spinner():
        fake_download()
