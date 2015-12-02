"""
Copyright 2015, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
from kivy.logger import Logger


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
