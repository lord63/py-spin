Py-Spin
=======

| |Latest Version|
| |Build Status|
| |Python Versions|

A little terminal spinner lib. Heavily inspired by `go-spin`_. (This library is not the one from FLIR).

Demo
----

|pyspin_demo|

Install
-------

::

    $ pip install pyspin

Usage
-----

make a spinner by hand:

.. code:: python

    from __future__ import print_function

    import sys
    import time

    from pyspin.spin import Default, Spinner

    # Choose a spin style.
    spin = Spinner(Default)
    # Spin it now.
    for i in range(50):
        print(u"\r{0}".format(spin.next()), end="")
        sys.stdout.flush()
        time.sleep(0.1)

or you can use the decorator pyspin provide:

.. code:: python

    from __future__ import print_function

    import time

    from pyspin.spin import make_spin, Default

    # Choose a spin style and the words when showing the spin.
    @make_spin(Default, "Downloading...")
    def download_video():
        time.sleep(10)

    if __name__ == '__main__':
        print("I'm going to download a video, and it'll cost much time.")
        download_video()
        print("Done!")

You can have a look at the example code in the example folder. Run it
via:

::

    $ python example/example_spin.py
    $ python example/usage_example.py

Contribute
----------

-  If you find an interesting spinner, send me a pull request <3
-  If you find a bug or have any suggestions, open an issue.

Contributions are always welcome at any time! ✨ 🍰 ✨

License
-------

MIT.

.. _go-spin: https://github.com/tj/go-spin

.. |Latest Version| image:: http://img.shields.io/pypi/v/pyspin.svg
   :target: https://pypi.python.org/pypi/pyspin
.. |Build Status| image:: https://travis-ci.org/lord63/py-spin.svg
   :target: https://travis-ci.org/lord63/py-spin
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/pyspin.svg
   :target: https://pypi.python.org/pypi/pyspin
.. |pyspin_demo| image:: https://cloud.githubusercontent.com/assets/5268051/7448038/ba152a8c-f241-11e4-86e0-50bc3b33bce5.gif
