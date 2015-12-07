Photobooth
==========

A Raspberry Pi photobooth application.

    $ python photobooth [arguments]

For a list of command line arguments, run photobooth with the -h flag:

    $ python photobooth -h

Requirements
------------

* Raspberry Pi running Raspian Jessie or newer.
* Raspberry Pi touchscreen.
* Python 2.7. (I could not get Kivy to work with Python 3)
* Kivy 1.9.0 (http://kivy.org) for Python.
* gphoto2, and libgphoto2 (sudo apt-get install gphoto2).
* gphoto2-compatible camera (tested with Canon D300 / Digital Rebel)
* Imagemagick (sudo apt-get install imagemagick).
* Photo printer (tested with Canon Selphy 910).
* Lots of light.
* Props!

License
-------

Copyright 2015, Andrew Lin.
All rights reserved.

This software is released under the BSD 3-clause license. See LICENSE.txt or
https://opensource.org/licenses/BSD-3-Clause for more information
