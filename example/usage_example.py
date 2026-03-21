#!/usr/bin/env python3

import time

from pyspin.spin import Default, Spinner, make_spin, Spin1


# Context manager — recommended usage.
def download_video():
    time.sleep(5)


if __name__ == '__main__':
    print("Downloading a video with context manager:")
    with Spinner(Default, "Downloading...", "Done!\n"):
        download_video()

    # Decorator — alternative usage.
    @make_spin(Spin1, "Downloading...")
    def download_video_with_decorator():
        time.sleep(5)

    print("Downloading a video with decorator:")
    download_video_with_decorator()
    print("Done!")
