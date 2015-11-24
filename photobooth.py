"""
Copyright 2015, andrew
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
import camera


def main():
    """Run the photobooth."""
    camera.capture('/tmp/foo.%C')

if __name__ == '__main__':
    main()
