"""
Copyright 2015, andrew
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
class Event(object):
    """State machine event."""


class StartEvent(Event):
    """Start event."""


class UpdateEvent(Event):
    """Countdown update event."""


class PhotoDownloaded(Event):
    """Photo downloaded from camera event."""


class PrintEvent(Event):
    """Print photos event."""


class CancelEvent(Event):
    """Cancel photos event."""


class PrintCompleteEvent(Event):
    """Photo print complete event."""