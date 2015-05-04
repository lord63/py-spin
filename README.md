# Py-Spin

[![Latest Version][1]][2]

A little terminal spinner lib. Heavily inspired by [go-spin][].

## Demo

![pyspin_demo][]

## Install

    $ pip install pyspin

## Usage

    from __future__ import print_function, unicode_literals
    
    import sys
    import time
    
    from pyspin import spin
    
    # Choose a spin style.
    spin = spin.Spinner(spin.Default)
    # Spin it now.
    for i in range(50):
        print("\r{0}".format(spin.next()), end="")
        sys.stdout.flush()
        time.sleep(0.1)

        
or you can use the decorator pyspin provide.

    from __future__ import print_function, unicode_literals

    from pyspin import spin
    from pyspin.spin import make_spin
    
    # Choose a spin style and the words when showing the spin.
    @make_spin(spin.Default, "say some words here...")
    def download_video():
        print("I'm downloading a video, and it'll cost much time.")
        time.sleep(10)
        print("Done!")
        
        
You can have a look at the example code in the example folder.

## License

MIT.


[1]: http://img.shields.io/pypi/v/pyspin.svg
[2]: https://pypi.python.org/pypi/pyspin
[go-spin]: https://github.com/tj/go-spin
[pyspin_demo]: https://cloud.githubusercontent.com/assets/5268051/7448038/ba152a8c-f241-11e4-86e0-50bc3b33bce5.gif