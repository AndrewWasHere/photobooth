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
from kivy.logger import Logger
from kivy.uix.screenmanager import NoTransition

from ui import ScreenMgr


class PhotoboothState(object):
    WAITING = 'waiting state'
    COUNTDOWN1 = 'countdown 1 state'
    PHOTO1 = 'photo 1 state'
    COUNTDOWN2 = 'countdown 2 state'
    PHOTO2 = 'photo 2 state'
    COUNTDOWN3 = 'countdown 3 state'
    PHOTO3 = 'photo 3 state'
    SELECTING = 'selecting state'
    PRINTING = 'printing state'

    def __init__(self):
        self.state = self.WAITING
        Logger.info('State Machine: Initialized to state %s', self.state)

    def transition_to(self, new_state):
        Logger.info(
            'State Machine: Transitioning from "%s" to "%s"',
            self.state,
            new_state
        )
        self.state = new_state


class PhotoboothApp(App):
    def __init__(self, settings, **kwargs):
        Logger.info('PhotoboothApp: __init__().')
        super(PhotoboothApp, self).__init__(**kwargs)
        self.settings = settings
        self.sm = None
        self.state_machine = PhotoboothState()
        self.countdown = None

    def build(self):
        """Build UI.

        User interface objects stored in the app must be created here, not in
        __init__().
        """
        Logger.info('PhotoboothApp: build().')
        self.sm = ScreenMgr(self, transition=NoTransition())
        return self.sm

    def start_event(self):
        """Waiting screen start button pressed."""
        Logger.info('PhotoboothApp: start_event().')
        self.state_machine.transition_to(PhotoboothState.COUNTDOWN1)
        self.sm.pb_screens[ScreenMgr.COUNTDOWN].start_countdown(
            self.settings.initial_wait_time
        )
        self.sm.current = ScreenMgr.COUNTDOWN

    def photo_event(self):
        """Time to take a picture."""
        Logger.info('PhotoboothApp: photo_event().')
        # if self.state_machine.state not in (
        #     PhotoboothState.COUNTDOWN1,
        #     PhotoboothState.COUNTDOWN2,
        #     PhotoboothState.COUNTDOWN3
        # ):
        #     Logger.error(
        #         'photo event occured in state %s',
        #         self.state_machine.state
        #     )
        #     return
        #
        # if self.state_machine.state == PhotoboothState.COUNTDOWN1:
        #     self.state_machine.transition_to(PhotoboothState.PHOTO1)
        # elif self.state_machine.state == PhotoboothState.COUNTDOWN2:
        #     self.state_machine.transition_to(PhotoboothState.PHOTO2)
        # else:
        #     self.state_machine.transition_to(PhotoboothState.PHOTO3)
        #
        # self.sm.current = ScreenMgr.CHEESE


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