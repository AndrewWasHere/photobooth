"""
Copyright 2015, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
import os
import random
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager

from ui.photoboothstate import PhotoboothState

LARGE_FONT = 130
SMALL_FONT = 50


class ScreenMgr(ScreenManager):
    """Screen Manager for the photobooth screens."""
    # Screen names.
    WAITING = 'waiting'
    COUNTDOWN = 'countdown'
    CHEESE = 'cheese'
    SELECTING = 'selecting'
    PRINTING = 'printing'

    def __init__(self, app, **kwargs):
        """
        Args:
            app (kivy.App):

        Returns:

        """
        Logger.info('ScreenMgr: __init__().')
        super(ScreenMgr, self).__init__(**kwargs)
        self.app = app
        self.pb_screens = {
            self.WAITING: WaitingScreen(app, name=self.WAITING),
            self.COUNTDOWN: CountdownScreen(app, name=self.COUNTDOWN),
            self.CHEESE: CheeseScreen(app, name=self.CHEESE),
            self.SELECTING: SelectingScreen(app, name=self.SELECTING),
            self.PRINTING: PrintingScreen(app, name=self.PRINTING)
        }
        for screen in self.pb_screens.itervalues():
            self.add_widget(screen)

        self.current = self.WAITING


class WaitingScreen(Screen):
    """Waiting state widget.

    +-----------------+
    |   Photobooth    |
    |                 |
    | Press to begin. |
    |                 |
    +-----------------+
    """
    def __init__(self, app, **kwargs):
        """
        Args:
            app (kivy.App):

        Returns:

        """
        Logger.info('WaitingScreen: __init__().')
        super(WaitingScreen, self).__init__(**kwargs)

        self.app = app
        self.start_button = Button(
            text='Photobooth\n==========\n\n\nPress to begin.',
            # text_size=self.size,
            halign='center',
            valign='top',
            font_size=SMALL_FONT,
            background_color=(0, 0, 1, 1)
        )
        self.start_button.bind(on_release=self.start_event)

        self.layout = BoxLayout()
        self.layout.add_widget(self.start_button)
        self.add_widget(self.layout)

    def start_event(self, obj):
        Logger.info('WaitingScreen: start_event(%s).', obj)
        self.app.start_event()


class CountdownScreen(Screen):
    """Countdown state widget.

    +-----------------+
    |                 |
    |        5        |
    |                 |
    |                 |
    +-----------------+
    """
    def __init__(self, app, **kwargs):
        """
        Args:
            app (kivy.App):

        Returns:

        """
        Logger.info('CountdownScreen: __init__().')
        super(CountdownScreen, self).__init__(**kwargs)

        self.app = app
        self.time_remaining = 5
        self.time_remaining_label = Label(
            text=str(self.time_remaining),
            # text_size=self.size,
            halign='center',
            valign='middle',
            font_size=LARGE_FONT
        )
        self.layout = BoxLayout()
        self.layout.add_widget(self.time_remaining_label)
        self.add_widget(self.layout)

    def timer_event(self, obj):
        Logger.info('CountdownScreen: timer_event(%s)', obj)
        self.time_remaining -= 1
        if self.time_remaining:
            self.time_remaining_label.text = str(self.time_remaining)
            Clock.schedule_once(self.timer_event, 1)

        else:
            self.app.photo_event()

    def start_countdown(self, time):
        Logger.info('CountdownScreen: start_countdown(%s)', time)
        self.time_remaining = time
        self.time_remaining_label.text = str(self.time_remaining)
        Clock.schedule_once(self.timer_event, 1)


class CheeseScreen(Screen):
    """Cheese state widget.

    +-----------------+
    |                 |
    |     Cheese!     |
    |                 |
    |                 |
    +-----------------+
    """
    smile = [
        'Cheese!',
        'Smile!',
        'Albatross!',
        'Rutabega!',
        'Bumfuzzle!',
        'Gardyloo!',
        'Taradiddle!',
        'Widdershins!',
        'Diphthong!'
    ]
    waiting = [
        '',
        'Processing...',
        '',
        'Still processing...',
        '',
        'Waiting on the camera...',
        '',
        'Almost done...',
        '',
        'Any second now...',
        ''
    ]

    def __init__(self, app, **kwargs):
        """
        Args:
            app:

        Returns:

        """
        Logger.info('CheeseScreen: __init__().')
        super(CheeseScreen, self).__init__(**kwargs)

        self.app = app
        self.smile_label = Label(
            text=self.smile[0],
            halign='center',
            valign='middle',
            font_size=LARGE_FONT
        )
        self.layout = BoxLayout()
        self.layout.add_widget(self.smile_label)
        self.add_widget(self.layout)

        self.wait_idx = 0
        self.wait_count = 0

    def on_entry(self):
        Logger.info('CheeseScreen: on_entry().')
        self.smile_label.font_size = LARGE_FONT
        self.smile_label.text = random.choice(self.smile)
        self.wait_idx = -1
        self.wait_count = 0
        Clock.schedule_once(self.timer_event, 2)

    def timer_event(self, obj):
        Logger.info('CheeseScreen: timer_event().')
        if self.app.processing():
            self.wait_count += 1
            if self.wait_count % 3 == 0:
                self.wait_idx = (self.wait_idx + 1) % len(self.waiting)
                self.smile_label.font_size = SMALL_FONT
                self.smile_label.text = self.waiting[self.wait_idx]

            Clock.schedule_once(self.timer_event, 1)
        else:
            self.app.photo_complete_event()


class SelectingScreen(Screen):
    """Selecting state widget.

    +-----------------+
    |+------+ +------+|
    ||  1   | |  2   ||
    |+------+ +------+|
    |+------+         |
    ||  3   | |Print| |
    |+------+ |Cancel||
    +-----------------+
    """
    def __init__(self, app, **kwargs):
        """
        Args:
            app:

        Returns:

        """
        Logger.info('CheeseScreen: __init__().')
        super(SelectingScreen, self).__init__(**kwargs)

        spacing = 10
        button_padding = [40, 40, 40, 40]
        photo_padding = [10, 10, 10, 10]

        self.app = app
        self.image1 = Image()
        self.image2 = Image()
        self.image3 = Image()
        self.print_button = Button(text='Print', background_color=(0, 1, 0, 1))
        self.cancel_button = Button(text='Cancel', background_color=(1, 0, 0, 1))

        self.print_button.bind(on_release=self.print_event)
        self.cancel_button.bind(on_release=self.cancel_event)

        top_row = BoxLayout(
            orientation='horizontal',
            spacing=spacing,
            padding=photo_padding
        )
        top_row.add_widget(self.image1)
        top_row.add_widget(self.image2)

        button_layout = BoxLayout(
            orientation='vertical',
            spacing=spacing,
            padding=button_padding
        )
        button_layout.add_widget(self.print_button)
        button_layout.add_widget(self.cancel_button)

        bottom_row = BoxLayout(orientation='horizontal', spacing=spacing)
        bottom_row.add_widget(self.image3)
        bottom_row.add_widget(button_layout)

        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(top_row)
        self.layout.add_widget(bottom_row)

        self.add_widget(self.layout)

    def on_entry(self):
        Logger.info('SelectingScreen: on_entry().')

        self.image1.source = self.app.photonames[PhotoboothState.PHOTO1]
        self.image2.source = self.app.photonames[PhotoboothState.PHOTO2]
        self.image3.source = self.app.photonames[PhotoboothState.PHOTO3]

    def cancel_event(self, obj):
        Logger.info('SelectingScreen: cancel_event().')
        self.app.cancel_event()

    def print_event(self, obj):
        Logger.info('SelectingScreen: print_event().')
        self.app.print_event()


class PrintingScreen(Screen):
    """Printing state widget.

    +-----------------+
    |                 |
    |   Printing...   |
    |                 |
    |                 |
    +-----------------+
    """
    statuses = ['Resizing...', 'Montaging...', 'Compositing...', 'Printing...']

    def __init__(self, app, **kwargs):
        """
        Args:
            app:

        Returns:

        """
        Logger.info('PrintingScreen: __init__().')
        super(PrintingScreen, self).__init__(**kwargs)

        self.app = app
        self.status = Label(
            text=self.statuses[0],
            halign='center',
            valign='middle',
            font_size=SMALL_FONT
        )
        layout = BoxLayout()
        layout.add_widget(self.status)
        self.add_widget(layout)

        self.idx = 0

    def on_entry(self):
        Logger.info('PrintingScreen: on_entry().')
        self.app.resize_images()
        Clock.schedule_once(self.timer_event, 0.5)

    def timer_event(self, obj):
        Logger.info('PrintingScreen: timer_event().')
        if self.idx == 0:
            # Resizing images.
            if not self.app.processing():
                self.idx += 1
                self.status.text = self.statuses[self.idx]
                self.app.compose_photo()

            Clock.schedule_once(self.timer_event, 0.5)

        elif self.idx == 1:
            # Montaging print.
            if not self.app.processing():
                self.idx += 1
                self.status.text = self.statuses[self.idx]
                self.app.composite_photo()

            Clock.schedule_once(self.timer_event, 0.5)

        elif self.idx == 2:
            # Compositing.
            if not self.app.processing():
                self.idx += 1
                self.status.text = self.statuses[self.idx]
                self.app.print_photo()

            Clock.schedule_once(self.timer_event, 0.5)

        else:
            # Printing.
            if not self.app.processing():
                self.idx = 0
                self.status.text = self.statuses[self.idx]
                self.app.print_complete()
            else:
                Clock.schedule_once(self.timer_event, 0.5)

