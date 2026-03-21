#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import threading
import time

import pytest

from pyspin import spin


class TtyStringIO(io.StringIO):
    def isatty(self):
        return True


class NonTtyStringIO(io.StringIO):
    def isatty(self):
        return False


class BareStream(object):
    def __init__(self):
        self._buf = []

    def write(self, s):
        self._buf.append(s)

    def getvalue(self):
        return ''.join(self._buf)


class BoolIsattyStream(BareStream):
    isatty = False


class FlushTrackingTtyStringIO(TtyStringIO):
    def __init__(self):
        super(FlushTrackingTtyStringIO, self).__init__()
        self.flush_count = 0

    def flush(self):
        self.flush_count += 1
        super(FlushTrackingTtyStringIO, self).flush()


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


def test_context_manager(monkeypatch):
    stdout = TtyStringIO()
    monkeypatch.setattr(spin.sys, 'stdout', stdout)

    def fake_download():
        threading.Event().wait(0.2)

    spinner = spin.Spinner()
    with spinner:
        fake_download()

    assert spinner.spin_thread is None
    assert spinner._stop_event is None
    assert stdout.getvalue()


def test_make_spin_custom_params(monkeypatch):
    stdout = TtyStringIO()
    monkeypatch.setattr(spin.sys, 'stdout', stdout)

    @spin.make_spin('+-', 'Downloading...', 'DONE')
    def fake_download():
        threading.Event().wait(0.2)

    fake_download()

    output = stdout.getvalue()
    assert 'Downloading...' in output
    assert 'DONE' in output
    assert '\r+    Downloading...' in output or '\r-    Downloading...' in output


def test_context_manager_stops_on_exception(monkeypatch):
    stdout = TtyStringIO()
    monkeypatch.setattr(spin.sys, 'stdout', stdout)
    spinner = spin.Spinner('+-', 'Downloading...', 'DONE')

    with pytest.raises(RuntimeError):
        with spinner:
            threading.Event().wait(0.2)
            raise RuntimeError('boom')

    assert spinner.spin_thread is None
    assert spinner._stop_event is None
    assert stdout.getvalue().endswith('DONE')


def test_context_manager_raises_when_reentered_while_running(monkeypatch):
    stdout = TtyStringIO()
    monkeypatch.setattr(spin.sys, 'stdout', stdout)
    spinner = spin.Spinner('+-', 'Downloading...', 'DONE')

    spinner.__enter__()
    try:
        with pytest.raises(RuntimeError, match="already running"):
            spinner.__enter__()
    finally:
        spinner.__exit__(None, None, None)


@pytest.mark.parametrize(
    'stdout_factory',
    [NonTtyStringIO, BareStream, BoolIsattyStream],
)
def test_no_output_when_stdout_is_not_a_tty(monkeypatch, stdout_factory):
    stdout = stdout_factory()
    monkeypatch.setattr(spin.sys, 'stdout', stdout)

    @spin.make_spin('+-', 'Downloading...', 'DONE')
    def fake_download():
        threading.Event().wait(0.2)

    fake_download()
    with spin.Spinner('+-', 'Downloading...', 'DONE'):
        threading.Event().wait(0.2)

    assert stdout.getvalue() == ''


def test_context_manager_reuse_after_tty_then_non_tty(monkeypatch):
    tty_stdout = TtyStringIO()
    monkeypatch.setattr(spin.sys, 'stdout', tty_stdout)
    spinner = spin.Spinner('+-', 'Downloading...', 'DONE')

    with spinner:
        threading.Event().wait(0.2)

    non_tty_stdout = NonTtyStringIO()
    monkeypatch.setattr(spin.sys, 'stdout', non_tty_stdout)

    with spinner:
        threading.Event().wait(0.2)

    assert spinner.spin_thread is None
    assert spinner._stop_event is None
    assert non_tty_stdout.getvalue() == ''


def test_make_spin_flushes_ending(monkeypatch):
    stdout = FlushTrackingTtyStringIO()
    monkeypatch.setattr(spin.sys, 'stdout', stdout)

    @spin.make_spin('+-', 'Downloading...', 'DONE')
    def fake_download():
        return 'ok'

    assert fake_download() == 'ok'
    output = stdout.getvalue()
    assert output.endswith('DONE')
    assert stdout.flush_count >= 1
