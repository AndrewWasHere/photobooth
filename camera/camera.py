"""
Copyright 2015, andrew
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
import shlex
import subprocess


def capture(filename):
    """Capture image from camera to file.

    File will be overwritten. You have been warned.

    Args:
        filename (str): File path to save image to.

    Returns:
        saved (str or list): File path saved. If more than one file is saved
        (raw and jpeg, for instance), a list is returned.

    Raises:
        subprocess.CalledProcessError: camera call failed.
    """
    # Command line arguments:
    # --capture-image-and-download: Take a picture and download it.
    # --filename {}: Name the image.
    # --keep: Keep image on camera.
    # --force-overwrite: Overwrite file if it exists.
    cmd = (
        'gphoto2 '
        '--capture-image-and-download '
        '--filename {filename} '
        '--keep '
        '--force-overwrite'.format(
           filename=filename
        )
    )
    cmd = shlex.split(cmd)
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    saved = _parse_output(output)
    return saved


def _parse_output(output):
    """Parse the gphoto2 output.

    Args:
        output (str): Ouput of gphoto2 call.

    Returns:
        saved_files (str or list): file path, if one file, list of file paths
            if multiple files.

    Raises (subprocess.CalledProcessError): gphoto2 error.
    """
    lines = output.split('\n')
    if '*** Error ***' in output:
        raise subprocess.CalledProcessError(lines[1])

    saved_files = [
        _extract_filename(l)
        for l in lines
        if l.startswith('Saving file as')
    ]

    if len(saved_files) == 1:
        saved_files = saved_files[0]

    return saved_files


def _extract_filename(line):
    """Extract filename from line of gphoto2 output.

    Assumption: line is of the form 'Saving file as <filename>'

    Args:
        line (str): Line of gphoto2 output.

    Returns:
        filename (str)
    """
    filename = line.split('as')[-1].strip()
    return filename
