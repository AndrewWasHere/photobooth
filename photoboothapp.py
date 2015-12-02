"""
Copyright 2015, andrew
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
import os
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.screenmanager import NoTransition

from camera import camera
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
        self.camera = None
        self.photobuffer = '/tmp/photobooth'
        self.photonames = {
            PhotoboothState.PHOTO1: 'photo1.jpg',
            PhotoboothState.PHOTO2: 'photo2.jpg',
            PhotoboothState.PHOTO3: 'photo3.jpg',
        }
        if not os.path.exists(self.photobuffer):
            os.makedirs(self.photobuffer)

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
        if self.state_machine.state not in (
            PhotoboothState.COUNTDOWN1,
            PhotoboothState.COUNTDOWN2,
            PhotoboothState.COUNTDOWN3
        ):
            Logger.error(
                'photo event occurred unexpectedly in "%s"',
                self.state_machine.state
            )
            return

        if self.state_machine.state == PhotoboothState.COUNTDOWN1:
            state = PhotoboothState.PHOTO1
        elif self.state_machine.state == PhotoboothState.COUNTDOWN2:
            state = PhotoboothState.PHOTO2
        else:
            state = PhotoboothState.PHOTO3

        # Update UI.
        self.sm.pb_screens[ScreenMgr.CHEESE].on_entry()
        self.sm.current = ScreenMgr.CHEESE

        # Take the picture.
        self.camera = camera.capture_background(
            os.path.join(self.photobuffer, self.photonames[state])
        )

        self.state_machine.transition_to(state)

    def photo_complete_event(self):
        """Camera finished taking picture."""
        Logger.info('PhotoboothApp: photo_complete_event().')

        if self.state_machine.state not in (
            PhotoboothState.PHOTO1,
            PhotoboothState.PHOTO2,
            PhotoboothState.PHOTO3
        ):
            Logger.error(
                'photo complete event occurred unexpectedly in "%s"',
                self.state_machine.state
            )
            return

        if self.state_machine.state == PhotoboothState.PHOTO1:
            state = PhotoboothState.COUNTDOWN2
            self.sm.pb_screens[ScreenMgr.COUNTDOWN].start_countdown(
                self.settings.wait_time
            )
            self.sm.current = ScreenMgr.COUNTDOWN
        elif self.state_machine.state == PhotoboothState.PHOTO2:
            state = PhotoboothState.COUNTDOWN3
            self.sm.pb_screens[ScreenMgr.COUNTDOWN].start_countdown(
                self.settings.wait_time
            )
            self.sm.current = ScreenMgr.COUNTDOWN
        else:
            if self.settings.skip_select:
                state = PhotoboothState.PRINTING
                self.sm.current = ScreenMgr.PRINTING
            else:
                state = PhotoboothState.SELECTING
                self.sm.current = ScreenMgr.SELECTING

        self.state_machine.transition_to(state)

    def camera_processing(self):
        """Check to see if camera is still processing the photo."""
        if self.camera and self.camera.poll() is None:
            # Still processing.
            return True

        return False
