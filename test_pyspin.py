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
        time.sleep(5)
    fake_download()
