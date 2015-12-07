"""
Copyright 2015, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
import os
import shlex
import subprocess

from kivy.app import App
from kivy.logger import Logger
from kivy.uix.screenmanager import NoTransition

from ui.photoboothstate import PhotoboothState
from ui.screens import ScreenMgr


class PhotoboothApp(App):
    def __init__(self, settings, **kwargs):
        Logger.info('PhotoboothApp: __init__().')

        super(PhotoboothApp, self).__init__(**kwargs)

        self.settings = settings
        self.sm = None
        self.state_machine = PhotoboothState()
        self.countdown = None
        self.processes = []
        photobuffer = '/tmp/photobooth'
        self.photonames = {
            PhotoboothState.PHOTO1: os.path.join(photobuffer, 'photo1.jpg'),
            PhotoboothState.PHOTO2: os.path.join(photobuffer, 'photo2.jpg'),
            PhotoboothState.PHOTO3: os.path.join(photobuffer, 'photo3.jpg'),
        }
        self.montage_image = os.path.join(photobuffer, 'montage.jpg')
        self.canvas_image = os.path.join(photobuffer, 'canvas.jpg')
        self.print_image = os.path.join(photobuffer, 'composite.jpg')
        if not os.path.exists(photobuffer):
            os.makedirs(photobuffer)

        cmd = (
            'convert '
            '-size 1800x1200 '
            'xc: {color} '
            '{filename}'.format(
                color=self.settings.background_color,
                filename=self.canvas_image
            )
        )
        subprocess.call(shlex.split(cmd))

    def build(self):
        """Build UI.

        User interface objects stored in the photoboothapp must be created here,
        not in __init__().
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
            self.sm.current = ScreenMgr.WAITING
            self.state_machine.transition_to(PhotoboothState.WAITING)
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
        self.capture_image(self.photonames[state])

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
            self.sm.current = ScreenMgr.WAITING
            self.state_machine.transition_to(PhotoboothState.WAITING)
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
                self.sm.pb_screens[ScreenMgr.PRINTING].on_entry()
                self.sm.current = ScreenMgr.PRINTING
            else:
                state = PhotoboothState.SELECTING
                self.sm.pb_screens[ScreenMgr.SELECTING].on_entry()
                self.sm.current = ScreenMgr.SELECTING

        self.state_machine.transition_to(state)

    def cancel_event(self):
        """Session canceled."""
        Logger.info('PhotoboothApp: cancel_event().')

        if self.state_machine.state != PhotoboothState.SELECTING:
            Logger.error(
                'cancel event occurred unexpectedly in "%s"',
                self.state_machine.state
            )

        self.sm.current = ScreenMgr.WAITING
        self.state_machine.transition_to(PhotoboothState.WAITING)

    def print_event(self):
        """Print request."""
        Logger.info('PhotoboothApp: print_event().')

        if self.state_machine.state != PhotoboothState.SELECTING:
            Logger.error(
                'print event occurred unexpectedly in "%s"',
                self.state_machine.state
            )
            self.sm.current = ScreenMgr.WAITING
            self.state_machine.transition_to(PhotoboothState.WAITING)
            return

        self.sm.pb_screens[ScreenMgr.PRINTING].on_entry()
        self.sm.current = ScreenMgr.PRINTING
        self.state_machine.transition_to(PhotoboothState.PRINTING)

    def capture_image(self, filename):
        """Launch process to capture image with camera."""
        Logger.info('PhotoboothApp: capture_image(%s).', filename)

        cmd = (
            'gphoto2 '
            '--capture-image-and-download '
            '--filename {filename} '
            '--keep '
            '--force-overwrite'.format(filename=filename)
        )
        cmd = shlex.split(cmd)
        self.processes = [subprocess.Popen(cmd)]

    def resize_images(self):
        """Launch processes to resize images."""
        Logger.info('PhotoboothApp: resize_images().')

        cmd = 'convert {src} -resize {width}x{height} {dest}'
        self.processes = [
            subprocess.Popen(
                shlex.split(
                    cmd.format(
                        src=fname,
                        width=880,
                        height=580,
                        dest=self.resized(fname)
                    )
                )
            )
            for fname in self.photonames.itervalues()
        ]

    def compose_photo(self):
        """Launch process to compose photo."""
        Logger.info('PhotoboothApp: compose_print().')

        cmd = (
            'montage {photo1} {photo2} {photo3} {logo} '
            '-mode concatenate '
            '-tile 2 '
            '-frame 10 '
            '-mattecolor none '
            '-background {background_color} '
            '{dest}'.format(
                photo1=self.resized(self.photonames[PhotoboothState.PHOTO1]),
                photo2=self.resized(self.photonames[PhotoboothState.PHOTO2]),
                photo3=self.resized(self.photonames[PhotoboothState.PHOTO3]),
                logo=self.settings.logo,
                background_color=self.settings.background_color,
                dest=self.montage_image
            )
        )
        self.processes = [subprocess.Popen(shlex.split(cmd))]

    def composite_photo(self):
        Logger.info('PhotoboothApp: composite_print().')

        cmd = (
            'composite '
            '-gravity center '
            '{montage} {canvas} {composite}'.format(
                montage=self.montage_image,
                canvas=self.canvas_image,
                composite=self.print_image
            )
        )
        self.processes = [subprocess.Popen(shlex.split(cmd))]

    def print_photo(self):
        """Launch process to print photo."""
        Logger.info('PhotoboothApp: print_photo().')

        self.processes = []

    def print_complete(self):
        """Print photo process complete."""
        Logger.info('PhotoboothApp: print_complete().')

        self.sm.current = ScreenMgr.WAITING
        self.state_machine.transition_to(PhotoboothState.WAITING)

    def processing(self):
        """Check to see if we are still composing the photo."""
        Logger.info('PhotoboothApp: processing().')

        if any((process.poll() is None for process in self.processes)):
            # Still processing.
            return True

        return False

    @staticmethod
    def resized(name):
        base, ext = os.path.splitext(name)
        return '{base}_resized{ext}'.format(base=base, ext=ext)
