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

import datetime

from ui.photoboothapp import PhotoboothApp


class PhotoboothSettings(object):
    """Container for settings."""
    def __init__(
        self,
        skip_select,
        save,
        initial_wait_time,
        wait_time,
        background_color,
        logo,
        printer
    ):
        self.skip_select = skip_select
        if save:
            save = os.path.abspath(os.path.expanduser(save))
            self.save = os.path.join(
                save,
                'photobooth_{}'.format(
                    datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                )
            )
        else:
            self.save = save

        self.initial_wait_time = initial_wait_time
        self.wait_time = wait_time
        self.background_color = background_color
        self.logo = os.path.abspath(os.path.expanduser(logo)) if logo else logo
        self.printer = printer


def parse_command_line():
    """Get settings from command line and/or config file."""
    config = ConfigParser.RawConfigParser()
    with open('photobooth_defaults.cfg') as fp:
        config.readfp(fp)

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
        '--save',
        default=None,
        help='Save composite photos to this directory. Photos are not saved if '
             'this flag is not specified. A new directory titled '
             'photobooth_<timestamp> will be added to the specified directory.'
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
    parser.add_argument(
        '--printer',
        default=None,
        help='Printer to print photos on. If not specified, photobooth will '
             'not print the photos (might want to use the --save flag in this '
             'case.'
    )

    args = parser.parse_args()
    if args.config:
        config.read(args.config)

    return PhotoboothSettings(
        skip_select=(
            args.skip_select or
            config.getboolean('photobooth', 'skip-select')
        ),
        save=(
            args.save or
            config.get('photobooth', 'save')
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
        ),
        printer=(
            args.printer
            if args.logo is not None else
            config.get('photobooth', 'printer')
        )
    )


def main():
    settings = parse_command_line()
    PhotoboothApp(settings).run()

if __name__ == '__main__':
    main()
