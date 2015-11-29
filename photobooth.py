"""
Copyright 2015, andrew
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
import ConfigParser
import argparse
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.logger import Logger


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


class Screens(ScreenManager):
    """Screen Manager for the photobooth screens.

    Defined in photobooth.kv
    """


class PhotoboothApp(App):
    def __init__(self, settings, **kwargs):
        Logger.info('PhotoboothApp: __init__()')
        super(PhotoboothApp, self).__init__(**kwargs)
        self.settings = settings
        self.sm = None

    def build(self):
        """Build UI.

        User interface objects stored in the app must be created here, not in
        __init__().
        """
        self.sm = Screens()
        return self.sm


class PhotoboothSettings(object):
    """Container for settings."""
    def __init__(self, skip_select, initial_wait_time, wait_time):
        self.skip_select = skip_select
        self.initial_wait_time = initial_wait_time
        self.wait_time = wait_time


def parse_command_line():
    """Get settings from command line and/or config file."""
    config = ConfigParser.RawConfigParser()
    config.readfp(open('photobooth_defaults.cfg'))

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config',
        default=None,
        help='Path to config file (command line arguments override settings).'
    )
    parser.add_argument(
        '--skip-select',
        action='store_true',
        help='Skip photo selection, and print all.'
    )
    parser.add_argument(
        '--initial-wait-time',
        type=int,
        default=None,
        help='Time to wait after start button pressed before first photo.'
    )
    parser.add_argument(
        '--wait-time',
        type=int,
        default=None,
        help='Time to wait between photos, after camera processing complete.'
    )
    args = parser.parse_args()
    if args.config:
        config.read(args.config)

    return PhotoboothSettings(
        skip_select=(
            args.skip_select or
            config.getboolean('photobooth', 'skip-select')
        ),
        initial_wait_time=(
            args.initial_wait_time
            if args.initial_wait_time is not None else
            config.getint('photobooth', 'initial-wait-time')
        ),
        wait_time=(
            args.wait_time
            if args.wait_time is not None else
            config.getint('photobooth', 'initial-wait-time')
        )
    )


def main():
    settings = parse_command_line()
    PhotoboothApp(settings).run()

if __name__ == '__main__':
    main()