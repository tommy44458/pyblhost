#!/usr/bin/env python
#
# Python implementation of blhost used to communicate with the NXP MCUBOOT/KBOOT bootloader.
# Copyright (C) 2020-2021  Kristian Sloth Lauszus.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Contact information
# -------------------
# Kristian Sloth Lauszus
# Web      :  https://www.lauszus.com
# e-mail   :  lauszus@gmail.com

import logging

from pyblhost import BlhostHid

def main():
    # BlhostCan specific arguments
    vid, pid = 8137, 33

    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
    logger.addHandler(stream_handler)

    # Specify the binary to upload, the start address to upload it to and the byte count to erase before uploading
    binary = 'BrainDyLPC55s69.bin'
    start_address, byte_count = 0x0, 0x34000

    with BlhostHid(vid, pid, logger) as blhost:
        old_progress = None
        result = False
        for progress in blhost.upload(binary, start_address, byte_count, timeout=1):
            if not isinstance(progress, bool):
                # The progress is returned as a float, so round the value in order to not spam the console
                progress = round(progress)
                if progress != old_progress:
                    old_progress = progress
                    logger.info('Upload progress: {} %'.format(progress))
            else:
                # The result will be returned as a boolean
                result = progress
        if result is True:
            logger.info('Uploading succeeded')
            exit(0)
        else:
            logger.error('Uploading failed')
            exit(1)


if __name__ == '__main__':
    main()
