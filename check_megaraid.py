#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# © Copyright 2014 Benjamin Heublein. All Rights Reserved.

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
#
# This program is released under the GNU General Public License, Version 3,
# with the additional exemption that compiling, linking and/or using OpenSSL
# is allowed.
"""This script is a nagios plugin for checking the state of megaraid controller

This script checks the state of physical discs and logical volumes plugged at a
megaraidcontroller.
It is inspired by check_megaraid_sas

"""
from __future__ import print_function

import argparse
import re
import subprocess
import sys

OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3

__version__ = "0.2"
__author__ = "Benjamin Heublein <bheublein@wavecon.de>"
__copyright__ = "© Copyright 2014 Benjamin Heublein"


BBU_CHARGING = "bbu_charging"
BBU_CHARGING_COUNT = "bbu_charging_count"
BBU_NAV = "bbu_nav"
BBU_NAV_COUNT = "bbu_nav_count"
BBU_NCHARGING = "bbu_ncharging"
BBU_NCHARGING_COUNT = "bbu_ncharging_count"
HOTSPARE_COUNT = "hotspare_count"
LOGICAL_DISK_ERRORS = "logical_disk_errors"
LOGICAL_DISK_COUNT = "logical_disk_count"
MEDIA_ERRORS = "media_errors"
OTHER_ERRORS = "other_errors"
PRED_ERRORS = "pred_errors"
PHYSICAL_ERRORS = "physical_errors"
PHYSICAL_DRIVES_COUNT = "physical_disk_count"

regex_ctrl_count = re.compile(r"Controller Count:\s*(\d+)")
regex_firmware_state = re.compile(r"Firmware state\s*:\s*(\w+)")
regex_logdrive_state = re.compile(r"State\s*:\s*(\w+)")
regex_media_other_errors = re.compile(r"(\w+) Error Count\s*:\s*(\d+)")
regex_num_vdrives = re.compile((r"Number of Virtual Drives"
                                r" Configured"
                                r" on Adapter \d:\s*(\d+)"))
regex_num_pdrives = re.compile((r"Number of Physical Drives"
                                r" on Adapter \d:\s*(\d+)"))
regex_predictive_errors = re.compile(r"Predictive Failure Count\s*:\s*(\d+)")
regex_bbu_charge_status = re.compile(r"Charging Status\s*:\s*(\w+)")
regex_bbu_not_charging = re.compile(r"Fully Charged\s*:\s*(\w+)")
regex_bbu_relativ_charge_state = re.compile(r"Relative State of "
                                            r"Charge\s*:\s*(\w+)")
regex_bbu_exit_code = re.compile("Exit Code\s*:\s*(\w+)")


def analyze_scanresult(scanresult, logical, physical, media, pred, other,
                       spares):
    """analyze the scanresult an return a statuscode and an output message

    Args:
        scanresult - all found drive errors
        logical - number of expected logical drives
        physical - number of expected physical drives
        media - number of media errors to ignore
        pred - number of predictive errors to ignore
        other - number of other errors to ignore
        spares - number of expected hotspares

    Returns:
       Statuscode an a return message

    """
    status = OK
    msg = ["(m{0}p{1}o{2})".format(scanresult[MEDIA_ERRORS],
                                   scanresult[PRED_ERRORS],
                                   scanresult[OTHER_ERRORS])]

    if scanresult[HOTSPARE_COUNT] < spares:
        status = increase_state(status, WARNING)
        msg.append(("Expected {0} Hotspares,"
                    " got {1}.".format(spares, scanresult[HOTSPARE_COUNT])))

    if (scanresult[MEDIA_ERRORS] > media
            or scanresult[PRED_ERRORS] > pred
            or scanresult[OTHER_ERRORS] > other):

        status = increase_state(status, WARNING)
        msg.append("Found diskerrors.")

    if scanresult[BBU_CHARGING_COUNT]:
        status = increase_state(status, WARNING)
        msg.append("{0} BBU charging.".format(scanresult[BBU_CHARGING_COUNT]))

    if scanresult[BBU_NCHARGING_COUNT]:
        status = increase_state(status, WARNING)
        msg.append(str(scanresult[BBU_NCHARGING_COUNT])+" BBU not charging.")

    if scanresult[BBU_NAV_COUNT]:
        status = increase_state(status, CRITICAL)
        msg.append("{0} BBU not available.".format(scanresult[BBU_NAV_COUNT]))

    if scanresult[PHYSICAL_ERRORS]:
        status = increase_state(status, CRITICAL)
        msg.append("Found {0} ".format(scanresult[PHYSICAL_ERRORS])
                   + "physical disk error(s).")

    if scanresult[LOGICAL_DISK_ERRORS]:
        status = increase_state(status, CRITICAL)
        msg.append("Found {0} logical ".format(scanresult[LOGICAL_DISK_ERRORS])
                   + "drive error(s).")

    if scanresult[LOGICAL_DISK_COUNT] < logical:
        status = increase_state(status, CRITICAL)
        msg.append("Missing logical Disk: "
                   + "Found {0} ".format(scanresult[LOGICAL_DISK_COUNT])
                   + "Expected {0}.".format(logical))

    if scanresult[PHYSICAL_DRIVES_COUNT] < physical:
        status = increase_state(status, CRITICAL)
        msg.append("Missing physical Disk: "
                   + "Found {0} ".format(scanresult[PHYSICAL_DRIVES_COUNT])
                   + "Expected {0}.".format(physical))

    if status == OK:
        msg.append("Everything is ok.")

    msg.reverse()  # reorder the msg so the most important comes first
    return (status, ' '.join(msg))


def count_controller():
    """count the built-in raid-controllers.

    Returns:
        number of built-in raid-controllers
    """
    count = regex_ctrl_count.search(execute(["-adpCount"]))

    if count:
        return int(count.group(1))
    return 0


def count_log_drives(controller):
    """count the logical drives on a given controller.

    Args:
        controller: The Number of the controller to count for its
                            logical drives

    Returns:
        number of logical drives
    """
    arg = regex_num_vdrives.search(execute(["-LdGetNum",
                                            "-a{0}".format(controller)]))
    if arg:
        return int(arg.group(1))
    return 0


def count_phys_drives(controller):
    """count the physical drives on a given controller.

    Args:
        controller: The Number of the controller to count for its
                            logical drives

    Returns:
    number of physical drives
    """
    arg = regex_num_pdrives.search(execute(["-PDGetNum",
                                            "-a{0}".format(controller)]))
    if arg:
        return int(arg.group(1))
    return 0


def execute(parameters):
    """excecute Megacli with the given Parameter and return its stdout.

    Args:
        parameters : interable sum of MegaCli parameters

    Returns:
        The stdout
    """
    cmd = ['sudo', 'MegaCli']
    cmd.extend(parameters)
    cmd.append("-NoLog")
    try:
        Bash = subprocess.Popen(cmd, stderr=subprocess.PIPE,
                                stdout=subprocess.PIPE)
        (out, err) = Bash.communicate()

    except OSError:
        print("Couldn't execute command: {}".format(" ".join(cmd)))
        sys.exit(UNKNOWN)
    except subprocess.CalledProcessError as err:
        print(err.output)
        sys.exit(UNKNOWN)

    if err:
        print("Couldn't execute command: {}".format(" ".join(cmd)))
        sys.exit(UNKNOWN)

    return out


def increase_state(old, new):
    """ compares two states and return the higher one

    Args:
        old - old state
        new - state
    Return:
        returns the higher state
    """
    return new if new > old else old


def scan_bbu(log):
    """ scan the given bbu log for it's status an errors

    Args:
        log -- detailed output log of megacli for this logical drive

    Return:
        {
        bbu_nav - number of not available  bbus on this adapter
        bbu_charging - number of charging bbus on this adapter
        bbu_ncharging - number of  not charging bbus on this adapter

    """
    bbu_nav = False
    bbu_charging = False
    bbu_ncharging = False

    # check exitcode
    status = regex_bbu_exit_code.search(log)
    if status and status.group(1) != '0x00':
        bbu_nav = True

    # check charging status
    else:
        status = regex_bbu_charge_status.search(log)
        if status and status.group(1) != 'None':
            bbu_charging = True

        else:
            # check not charching
            status = regex_bbu_not_charging.search(log)
            if status and status.group(1) != 'Yes':
                bbu_ncharging = True

    return {BBU_NAV: bbu_nav,
            BBU_CHARGING: bbu_charging,
            BBU_NCHARGING: bbu_ncharging}


def scan_logical_drive(log):
    """ scan the given logdrive log for errors

    Args:
        log -- detailed output log of megacli for this logical drive
    Return:
        True -> if a non-optimal state is found
        False -> if no or a optimal stat  is found
    """
    state = regex_logdrive_state.search(log)
    if state and state.group(1) != "Optimal":
            return True
    return False


def scan_physical_drive(log):
    """scan all physical Drives on the given controller.

    Args:
        log -- status log of all physical drives on a controller

    Return:
        Found media,other,predictive an physical errors and found hotspares
    """
    media = 0
    other = 0
    pred = 0
    physical = 0
    hotspares = 0

    moerror = regex_media_other_errors.findall(log)
    for entry in moerror:
        if entry[0] == "Media":
            media += int(entry[1])
        else:
            other += int(entry[1])

    pred_errors = regex_predictive_errors.findall(log)
    for entry in pred_errors:
        pred += int(entry[0])

    firmware_state = regex_firmware_state.findall(log)
    for entry in firmware_state:
        if entry:
            if entry == "Hotspare":
                hotspares += 1
            elif entry in ["Failed", "not"]:
                physical += 1
            elif entry not in ["Unconfigured", "Online"]:
                print("A Physical drive has an unknown Firmwarestatus" +
                      " '{0}'.".format(entry))
                sys.exit(UNKNOWN)

    return (media, other, pred, physical, hotspares)


def scan_controller(bbu_scan=False):
    """ Scan on all built-in controllerss all logical and physical drives.

    Args:
        bbu_scan - set true to scan the bbu. Default: false
    Returns:
        a dictionaray with
        LOGICAL_DISK_ERRORS: logical_errors
        PRED_ERRORS: predictive_errors
        OTHER_ERRORS: other_errors
        MEDIA_ERRORS: media_errors
        PHYSICAL_ERRORS: physical_errors
        HOTSPARECOUNT: number of found hotspares
        BBU_NAV_COUNT: number of not available bbus
        BBU_CHARGING_COUNT: number of bbus that are not charging
        BBU_NCHARGING_COUNT: number of bbus that are not charging
    """
    result = {LOGICAL_DISK_ERRORS: 0,
              LOGICAL_DISK_COUNT: 0,
              PHYSICAL_DRIVES_COUNT: 0,
              PRED_ERRORS: 0,
              OTHER_ERRORS: 0,
              MEDIA_ERRORS: 0,
              PHYSICAL_ERRORS: 0,
              HOTSPARE_COUNT: 0,
              BBU_NAV_COUNT: 0,
              BBU_CHARGING_COUNT: 0,
              BBU_NCHARGING_COUNT: 0
              }

    for controller in range(count_controller()):
        if bbu_scan:
            bbu_tmp = scan_bbu(execute(["-AdpBbuCmd",
                                        "-GetBbuStatus",
                                        "-a{0}".format(controller)]))
            result[BBU_NAV_COUNT] += int(bbu_tmp[BBU_NAV])
            result[BBU_CHARGING_COUNT] += int(bbu_tmp[BBU_CHARGING])
            result[BBU_NCHARGING_COUNT] += int(bbu_tmp[BBU_NCHARGING])

        phys_tmp = scan_physical_drive(execute(["-PdList",
                                                "-a{0}".format(controller)]))
        result[MEDIA_ERRORS] += phys_tmp[0]
        result[OTHER_ERRORS] += phys_tmp[1]
        result[PRED_ERRORS] += phys_tmp[2]
        result[PHYSICAL_ERRORS] += phys_tmp[3]
        result[HOTSPARE_COUNT] += phys_tmp[4]

        result[PHYSICAL_DRIVES_COUNT] += count_phys_drives(controller)
        logical_disks_count = count_log_drives(controller)
        result[LOGICAL_DISK_COUNT] += logical_disks_count
        for logdrive in range(logical_disks_count):
            tmp = scan_logical_drive(execute(["-LdInfo",
                                              "-L{0}".format(logdrive),
                                              "-a{0}".format(controller)]))
            result[LOGICAL_DISK_ERRORS] += int(tmp)
    return result


def main():
    """ simple main function.

    Returns:
            0 -> OK
            1 -> Warning
            2 -> Critical
            3 -> Unknown
    """

    # build the parser
    parser = argparse.ArgumentParser(description=("nagios-check for"
                                                  " megaraid-controllers"),
                                     )
    parser.add_argument("-b", "--bbu", action='store_true',
                        help="check the bbu", dest="scan_bbu")
    parser.add_argument("-s", "--spares", type=int,
                        help="expected number of hotspares at the controllers",
                        default=0)
    parser.add_argument("-l", "--logical", type=int,
                        help=(("expected number of logical disks at all "
                               "controllers")),
                        default=0)
    parser.add_argument("-d", "--disks", type=int,
                        help=(("expected number of physical disks at all "
                               "controllers")),
                        default=0)

    parser.add_argument("-m", "--media", type=int,
                        help="number of media errors to ignore",
                        default=0)
    parser.add_argument("-p", "--predictive", type=int,
                        help="number of predictiv errors to ignore",
                        default=0)
    parser.add_argument("-o", "--other", type=int,
                        help="number of other disk errors to ignore",
                        default=0)
    parser.add_argument("--version", action="version", version=__version__)

    # get parsed options
    options = parser.parse_args()

    # scan the controller
    scanresult = scan_controller(options.scan_bbu)

    # analyze result
    status, msg = analyze_scanresult(scanresult,
                                     options.logical,
                                     options.disks,
                                     options.media,
                                     options.predictive,
                                     options.other,
                                     options.spares)

    print(msg)
    return status

if __name__ == '__main__':
    sys.exit(main())
