Version numbers are following the Semantic Versioning.

2026.03.21 v1.2.0
- add
    - context manager support for Spinner, thanks to @liiight 
- fix
    - flush ending output in make_spin
    - harden TTY detection (support non-callable isatty and bool isatty)
- change
    - drop Python 2.x support
    - require Python 3.10+
- other
    - migrate from Travis CI to GitHub Actions
    - migrate from pip/setup.py to uv

2017.04.13 v1.1.1
- fix
    - fix incorrect futures requirement, thanks to @xoviat

2017.02.14 v1.1.0
- add
    - python3.6 support
- fix(see pr#9, thanks to @fruch)
    - fix infinite spin when exception happens
    - fix functions with args

2016.07.15 v1.0.2
- clear queue, see #6, thanks to @tschaume

2016.02.17 v1.0.1
- fix:
    - add the missing python 3.5 support in setup.py
- improve the `Spinner.next`

2015.12.15 v1.0.0
- add
    - python3.5 support
    - wheel support
- break change:
    - remove `Spinner.stop`
    - remove `Spinner.animate`
- fix:
    - under python3.x, the print message has 'b' prefix
    - 2.x unicode error

2015.05.04 v0.1.0
- initial release
