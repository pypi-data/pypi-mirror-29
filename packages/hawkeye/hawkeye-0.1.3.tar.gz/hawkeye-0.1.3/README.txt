===========
HawkEye
===========

HawkEye is a v of commands that I have been building up over time to save time. Turning four&five-liners into a quick, callable function.

HawkEye::

    #!/usr/bin/env python

    from hawkeye import *

    # quickly initialize a database (dictionary) and start storing things.

    _data = INIT_Database("<DesiredPathname>") # can be .txt or .json or a custom file
    printData(_data) # prettyprint
    _navigateData = navigate(_data) # prints keys of dictionary to console so you can find what you need quickly

I'm still working on it tho.