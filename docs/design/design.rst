==========
Photobooth
==========

Photobooth is a software application, when used in conjunction with the
appropriate hardware, that allows a user to take and print pictures like
a photobooth.

The software was written to run on a Raspberry Pi, though in reality, any
Linux machine should do (and will probably do better, since the Raspberry Pi
is a low-powered CPU). In fact, initial development was done on an Ubuntu 15.10
box.

Hardware Connections
====================

The original design was to have the photobooth as a stand-alone system, with
a touch display, camera, and photo printer attached to a Raspberry Pi.

.. uml::

    @startuml
    title Stand-Alone Setup

    [Touch Display] -- [Raspberry Pi]
    [Raspberry Pi] - [Camera] : USB
    [Raspberry Pi] -- [Printer] : USB
    @enduml

However, with limited printer drivers available at the time, printing directly
from the Raspberry Pi was problematic, so the capability for offline printing
was added to the code, and enabling ssh on the Raspberry Pi.

.. uml::
    @startuml
    title Network Setup

    [Touch Display] -- [Raspberry Pi]
    [Raspberry Pi] - [Camera] : USB
    [Raspberry Pi] .. [Computer] : Network
    [Computer] - [Printer] : USB
    @enduml

When it is time to print, the user can ssh into the Raspberry Pi, scp the
images, and print them from a more capable computer.

Design
======

The photobooth is essentially a state machine that moves between an idle state
a photo-taking state, a photo selecting state, and a printing state.

.. uml::

    @startuml
    ' Idle state
    [*] --> waiting
    waiting : on entry: display start screen
    waiting --> countdown : start event

    ' Shooting states
    countdown : on entry: update time remaining
    countdown --> countdown : update[time remaining]
    countdown --> cheese : update[no time remaining] |\n take photo
    cheese --> cheese : timer | refresh screen
    cheese --> countdown : photo downloaded\n[pictures remaining]

    ' Output states
    cheese --> selecting : photo downloaded\n[no pictures remaining]
    cheese --> printing : photo downloaded\n[no pictures remaining,\n skip selection]
    selecting --> printing : print event
    selecting --> waiting : cancel event
    printing --> waiting : print complete
    printing : on entry: resize, montage, composite, and print photo
    @enduml

Libraries
=========

Two libraries are used by Photobooth: gphoto2 and Kivy.

gPhoto2
-------

http://www.gphoto.org/

gPhoto2 is a library to control digital cameras with a computer over USB. Camera
settings can be modified, pictures taken, and photos downloaded off the camera
using gPhoto2 interfaces.

There are a couple gPhoto2 Python bindings available. I didn't like either of
them, so I just wrapped the command line interfaces I needed with Python
functions.

Kivy
----

https://kivy.org/

Kivy is a multi-touch-friendly GUI Python library that runs on many platforms
including Raspberry Pi. It does not piggy back on another windowing system, so
I could launch Photobooth at boot up with a cron job.

Spinning up a Kivy app is pretty straightforward, and since I was using the
Raspberry Pi Foundation's 7-inch touch screen, Kivy seemed like a good match.

Kivy has some other useful features such as a clock module for one-shot and
periodic timer events. The ScreenManager class manages multiple screens in an
application.