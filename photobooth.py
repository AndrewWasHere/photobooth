"""
Copyright 2015, andrew
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
import ConfigParser
import argparse

from photoboothapp import PhotoboothApp


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
            config.getint('photobooth', 'wait-time')
        )
    )


def main():
    settings = parse_command_line()
    PhotoboothApp(settings).run()

if __name__ == '__main__':
    main()
