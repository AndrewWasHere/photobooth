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

Design
======

The photobooth is essentially a state machine that moves between an idle state
a photo-taking state, a photo selecting state, and a printing state.

.. uml::

    @startuml
    [*] --> waiting
    waiting : on entry: display start screen
    waiting --> shooting : start event

    state shooting {
    [*] --> countdown
    countdown : on entry: update time remaining
    countdown --> countdown : update[time remaining]
    countdown --> cheese : update[no time remaining]
    cheese : on entry: take photo
    cheese --> countdown : photo downloaded[pictures remaining]
    }
    cheese --> selecting : photo downloaded[no pictures remaining]
    selecting --> printing : print event
    selecting --> waiting : cancel event
    printing --> waiting : print complete
    printing : on entry: print photo
    @enduml

Kivy
====

Kivy has a clock module for one-shot and periodic timer events.
ScreenManager manages multiple screens in an application