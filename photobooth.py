"""
Copyright 2015, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
import ConfigParser
import argparse
import os

from ui.photoboothapp import PhotoboothApp


class PhotoboothSettings(object):
    """Container for settings."""
    def __init__(
        self,
        skip_select,
        initial_wait_time,
        wait_time,
        background_color,
        logo
    ):
        self.skip_select = skip_select
        self.initial_wait_time = initial_wait_time
        self.wait_time = wait_time
        self.background_color = background_color
        self.logo = os.path.abspath(os.path.expanduser(logo)) if logo else logo


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
    parser.add_argument(
        '--background-color',
        default=None,
        help='Background color of photobooth print. Supported values are listed '
             'on http://www.imagemagick.org/script/color.php. You can also '
             'supply an RGB, or RGBA value using the notation "rgb(r, g, b)" '
             'or "rgba(r, g, b, a)", where r, g, b are integers between 0 and '
             '255, and a is a float between 0.0 and 1.0.'
    )
    parser.add_argument(
        '--logo',
        default=None,
        help='Path to logo to print on photograph.'
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
        ),
        background_color=(
            args.background_color
            if args.background_color is not None else
            config.get('photobooth', 'background-color')
        ),
        logo=(
            args.logo
            if args.logo is not None else
            config.get('photobooth', 'logo')
        )
    )


def main():
    settings = parse_command_line()
    PhotoboothApp(settings).run()

if __name__ == '__main__':
    main()
