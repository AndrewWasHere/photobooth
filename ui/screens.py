"""
Copyright 2015, andrew
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager


class ScreenMgr(ScreenManager):
    """Screen Manager for the photobooth screens."""
    WAITING = 'waiting'
    COUNTDOWN = 'countdown'

    def __init__(self, app, **kwargs):
        """
        Args:
            app (kivy.App):
            **kwargs (dict): ScreenManager parameters.

        Returns:

        """
        Logger.info('ScreenMgr: __init__().')
        super(ScreenMgr, self).__init__(**kwargs)
        self.app = app
        self.pb_screens = {
            self.WAITING: WaitingScreen(app, name=self.WAITING),
            self.COUNTDOWN: CountdownScreen(app, name=self.COUNTDOWN)
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
    def __init__(self, app, *args, **kwargs):
        """
        Args:
            app (kivy.App):
            **kwargs:

        Returns:

        """
        Logger.info('WaitingScreen: __init__().')
        super(WaitingScreen, self).__init__(*args, **kwargs)

        self.app = app
        self.start_button = Button(
            text='Photobooth\n==========\n\n\nPress to begin.',
            # text_size=self.size,
            halign='center',
            valign='top',
            font_size=50
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
    def __init__(self, app, *args, **kwargs):
        Logger.info('CountdownScreen: __init__().')
        super(CountdownScreen, self).__init__(*args, **kwargs)

        self.app = app
        self.time_remaining = 5
        self.time_remaining_label = Label(
            text=str(self.time_remaining),
            # text_size=self.size,
            halign='center',
            valign='top',
            font_size=50
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
        self.time_remaining = time
        self.time_remaining_label.text = str(self.time_remaining)
        Clock.schedule_once(self.timer_event, 1)


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
