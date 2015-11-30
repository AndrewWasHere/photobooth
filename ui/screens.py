"""
Copyright 2015, andrew
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
from kivy.uix.screenmanager import Screen, ScreenManager


class ScreenMgr(ScreenManager):
    """Screen Manager for the photobooth screens.

    Defined in photobooth.kv
    """
    def __init__(self, **kwargs):
        super(ScreenMgr, self).__init__(**kwargs)


class WaitingScreen(Screen):
    """Waiting state widget.

    Defined in photobooth.kv
    """


class CountdownScreen(Screen):
    """Countdown state widget.

    Defined in photobooth.kv
    """


class CheeseScreen(Screen):
    """Cheese state widget.

    Defined in photobooth.kv
    """


class SelectingScreen(Screen):
    """Selecting state widget.

    Defined in photobooth.kv
    """


class PrintingScreen(Screen):
    """Printing state widget.

    Defined in photobooth.kv
    """
