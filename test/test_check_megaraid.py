#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__version__ = "0.1"
__author__ = "Benjamin Heublein <bheublein@wavecon.de>"
__copyright__ = "© Copyright 2014 Benjamin Heublein"

import mock

from check_megaraid import scan_logical_drive, scan_physical_drive
from check_megaraid import analyze_scanresult, scan_controller, scan_bbu
from check_megaraid import count_controller, count_log_drives
from check_megaraid import count_phys_drives
from nose.tools import assert_equals
# testscript for check_megaraid.py


def test_function_scan_logical_drive_logical_drive_error():
    assert_equals(scan_logical_drive(("Virtual Drive: 1 (Target Id: 1)\n"
                                      "Name                :"
                                      "RAID Level          : Primary-1,"
                                      "Secondary-0, RAID Level"
                                      "Qualifier-0\n"
                                      "Size                : 4.362 TB\n"
                                      "State               : Degraded\n"
                                      "Strip Size          : 64 KB\n"
                                      "Number Of Drives per span:2\n"
                                      "Span Depth          : 8\n"
                                      "Default Cache Policy: WriteBack,"
                                      "ReadAdaptive, Direct,"
                                      "No Write Cache "
                                      "if Bad BBU\n"
                                      "Current Cache Policy: WriteBack,"
                                      "ReadAdaptive, Direct,"
                                      " No Write Cache"
                                      "if Bad BBU\n"
                                      "Access Policy       "
                                      ": Read/Write\n"
                                      "Disk Cache Policyi"
                                      " Disk's Default\n"
                                      "Encryption Type     : None\n"
                                      "Default Power Savings Policy:"
                                      " Controller Defined\n"
                                      " Current Power Savings"
                                      " Policy: None\n"
                                      "Can spin up in 1 minute: Yes\n"
                                      "LD has drives that support T10 "
                                      "power conditions: Yes\n"
                                      "LD's IO profile supports"
                                      " MAX power "
                                      "savings with cached writes: No\n"
                                      "Bad Blocks Exist: No\n")),
                  True)


def test_function_scan_logical_drive_logical_drive_ok():
    assert_equals(scan_logical_drive(("Virtual Drive: 1 (Target Id: 1)\n"
                                      "Name                :"
                                      "RAID Level          : Primary-1,"
                                      "Secondary-0, RAID Level"
                                      "Qualifier-0\n"
                                      "Size                : 4.362 TB\n"
                                      "State               : Optimal\n"
                                      "Strip Size          : 64 KB\n"
                                      "Number Of Drives per span:2\n"
                                      "Span Depth          : 8\n"
                                      "Default Cache Policy: WriteBack,"
                                      "ReadAdaptive, Direct,"
                                      "No Write Cache "
                                      "if Bad BBU\n"
                                      "Current Cache Policy: WriteBack,"
                                      "ReadAdaptive, Direct,"
                                      " No Write Cache"
                                      "if Bad BBU\n"
                                      "Access Policy       "
                                      ": Read/Write\n"
                                      "Disk Cache Policyi"
                                      " Disk's Default\n"
                                      "Encryption Type     : None\n"
                                      "Default Power Savings Policy:"
                                      " Controller Defined\n"
                                      " Current Power Savings"
                                      " Policy: None\n"
                                      "Can spin up in 1 minute: Yes\n"
                                      "LD has drives that support T10 "
                                      "power conditions: Yes\n"
                                      "LD's IO profile supports"
                                      " MAX power "
                                      "savings with cached writes: No\n"
                                      "Bad Blocks Exist: No\n")),
                  False)


def test_function_scan_physical_drive_media_errors():
    assert_equals(scan_physical_drive(("Adapter #0\n\n"
                                       "Enclosure Device ID: 32\n"
                                       "Slot Number: 0\n"
                                       "Enclosure position: 0\n"
                                       "Device Id: 0\n"
                                       "Sequence Number: 2\n"
                                       "Media Error Count: 1\n"
                                       "Other Error Count: 0\n"
                                       "Predictive "
                                       "Failure Count: 0\n"
                                       "Last Predictive Failure "
                                       "Event Seq Number: 0\n"
                                       "PD Type: SATA\n"
                                       "Raw Size: 93.160 GB "
                                       "[0xba52230 Sectors]\n"
                                       "Non Coerced Size: 92.660 "
                                       "GB [0xb952230 Sectors]\n"
                                       "Coerced Size: 92.625 GB "
                                       "[0xb940000 Sectors]\n"
                                       "Firmware state: Online, "
                                       "Spun Up\n"
                                       "SAS Address(0): "
                                       "0x500056b37789abe3\n"
                                       "Connected Port Number: "
                                       "0(path0)\n"
                                       "Inquiry Data:   "
                                       "BTTV412301EN100FGNINTEL \n"
                                       "SSDSC2BA100G3T\t5DV1DL05\n"
                                       "FDE Capable: Not Capable\n"
                                       "FDE Enable: Disable\n"
                                       "Secured: Unsecured\n"
                                       "Locked: Unlocked\n"
                                       "Needs EKM Attention: No\n"
                                       "Foreign State: None\n"
                                       "Device Speed: 3.0Gb/s\n"
                                       "Link Speed: 3.0Gb/s\n"
                                       "Media Type: Solid State "
                                       "Device\n"
                                       "Drive Temperature :25C "
                                       "(77.00 F)\n")),
                  (1, 0, 0, 0, 0))


def test_function_scan_physical_drive_other_errors():
    assert_equals(scan_physical_drive("Adapter #0\n\n"
                                      + "Enclosure Device ID: 32\n"
                                      + "Slot Number: 0\n"
                                      + "Enclosure position: 0\n"
                                      + "Device Id: 0\n"
                                      + "Sequence Number: 2\n"
                                      + "Media Error Count: 0\n"
                                      + "Other Error Count: 2\n"
                                      + "Predictive "
                                      + "Failure Count: 0\n"
                                      + "Last Predictive Failure "
                                      + "Event Seq Number: 0\n"
                                      + "PD Type: SATA\n"
                                      + "Raw Size: 93.160 GB "
                                      + "[0xba52230 Sectors]\n"
                                      + "Non Coerced Size: 92.660 "
                                      + "GB [0xb952230 Sectors]\n"
                                      + "Coerced Size: 92.625 GB "
                                      + "[0xb940000 Sectors]\n"
                                      + "Firmware state: Online, "
                                      + "Spun Up\n"
                                      + "SAS Address(0): "
                                      + "0x500056b37789abe3\n"
                                      + "Connected Port Number: "
                                      + "0(path0)\n"
                                      + "Inquiry Data:   "
                                      + "BTTV412301EN100FGNINTEL \n"
                                      + "SSDSC2BA100G3T\t5DV1DL05\n"
                                      + "FDE Capable: Not Capable\n"
                                      + "FDE Enable: Disable\n"
                                      + "Secured: Unsecured\n"
                                      + "Locked: Unlocked\n"
                                      + "Needs EKM Attention: No\n"
                                      + "Foreign State: None\n"
                                      + "Device Speed: 3.0Gb/s\n"
                                      + "Link Speed: 3.0Gb/s\n"
                                      + "Media Type: Solid State "
                                      + "Device\n"
                                      + "Drive Temperature :25C "
                                      + "(77.00 F)\n"),
                  (0, 2, 0, 0, 0))


def test_function_scan_bbu_not_charching():
    testtxt = ("BBU status for Adapter: 0\n\n"
               " BatteryType: BBU\n"
               "Voltage: 3909 mV\n"
               "Current: 0 mA\n"
               "Temperature: 42 C\n\n"
               "BBU Firmware Status:\n\n"
               "  Charging Status              : None\n"
               "  Voltage                                 : OK\n"
               "  Temperature                             : OK\n"
               "  Learn Cycle Requested                   : No\n"
               "  Learn Cycle Active                      : No\n"
               "  Learn Cycle Status                      : OK\n"
               "  Learn Cycle Timeout                     : No\n"
               "  I2c Errors Detected                     : No\n"
               "  Battery Pack Missing                    : No\n"
               "  Battery Replacement required            : No\n"
               "  Remaining Capacity Low                  : No\n"
               "  Periodic Learn Required                 : No\n"
               "  Transparent Learn                       : No\n"
               "  No space to cache offload               : No\n"
               "  Pack is about to fail & should be replaced : No\n"
               "  Cache Offload premium feature required  : No\n"
               "  Module microcode update required        : No\n\n"
               "Battery state: \n\n"
               "GasGuageStatus:\n"
               "  Fully Discharged        : No\n"
               "  Fully Charged           : No\n"
               "  Discharging             : No\n"
               "  Initialized             : No\n"
               "  Remaining Time Alarm    : Yes\n"
               "  Remaining Capacity Alarm: No\n"
               "  Discharge Terminated    : No\n"
               "  Over Temperature        : No\n"
               "  Charging Terminated     : No\n"
               "  Over Charged            : No\n\n"
               "Relative State of Charge: 92 %\n"
               "Charger Status: Complete\n"
               "Remaining Capacity: 540 mAh\n"
               "Full Charge Capacity: 593 mAh\n"
               "isSOHGood: Yes\n\n"
               "Exit Code: 0x00")
    assert_equals(scan_bbu(testtxt), {"bbu_nav": False,
                                      "bbu_charging": False,
                                      "bbu_ncharging": True})


def test_function_scan_bbu_charching():
    testtxt = ("BBU status for Adapter: 0\n\n"
               " BatteryType: BBU\n"
               "Voltage: 3909 mV\n"
               "Current: 0 mA\n"
               "Temperature: 42 C\n\n"
               "BBU Firmware Status:\n\n"
               "  Charging Status              : Charching\n"
               "  Voltage                                 : OK\n"
               "  Temperature                             : OK\n"
               "  Learn Cycle Requested                   : No\n"
               "  Learn Cycle Active                      : No\n"
               "  Learn Cycle Status                      : OK\n"
               "  Learn Cycle Timeout                     : No\n"
               "  I2c Errors Detected                     : No\n"
               "  Battery Pack Missing                    : No\n"
               "  Battery Replacement required            : No\n"
               "  Remaining Capacity Low                  : No\n"
               "  Periodic Learn Required                 : No\n"
               "  Transparent Learn                       : No\n"
               "  No space to cache offload               : No\n"
               "  Pack is about to fail & should be replaced : No\n"
               "  Cache Offload premium feature required  : No\n"
               "  Module microcode update required        : No\n\n"
               "Battery state: \n\n"
               "GasGuageStatus:\n"
               "  Fully Discharged        : No\n"
               "  Fully Charged           : No\n"
               "  Discharging             : No\n"
               "  Initialized             : No\n"
               "  Remaining Time Alarm    : Yes\n"
               "  Remaining Capacity Alarm: No\n"
               "  Discharge Terminated    : No\n"
               "  Over Temperature        : No\n"
               "  Charging Terminated     : No\n"
               "  Over Charged            : No\n\n"
               "Relative State of Charge: 92 %\n"
               "Charger Status: Complete\n"
               "Remaining Capacity: 540 mAh\n"
               "Full Charge Capacity: 593 mAh\n"
               "isSOHGood: Yes\n\n"
               "Exit Code: 0x00")
    assert_equals(scan_bbu(testtxt), {"bbu_charging": True,
                                      "bbu_nav": False,
                                      "bbu_ncharging": False})


def test_function_scan_bbu_fully_charged():
    testtxt = ("BBU status for Adapter: 0\n\n"
               " BatteryType: BBU\n"
               "Voltage: 3909 mV\n"
               "Current: 0 mA\n"
               "Temperature: 42 C\n\n"
               "BBU Firmware Status:\n\n"
               "  Charging Status              : None\n"
               "  Voltage                                 : OK\n"
               "  Temperature                             : OK\n"
               "  Learn Cycle Requested                   : No\n"
               "  Learn Cycle Active                      : No\n"
               "  Learn Cycle Status                      : OK\n"
               "  Learn Cycle Timeout                     : No\n"
               "  I2c Errors Detected                     : No\n"
               "  Battery Pack Missing                    : No\n"
               "  Battery Replacement required            : No\n"
               "  Remaining Capacity Low                  : No\n"
               "  Periodic Learn Required                 : No\n"
               "  Transparent Learn                       : No\n"
               "  No space to cache offload               : No\n"
               "  Pack is about to fail & should be replaced : No\n"
               "  Cache Offload premium feature required  : No\n"
               "  Module microcode update required        : No\n\n"
               "Battery state: \n\n"
               "GasGuageStatus:\n"
               "  Fully Discharged        : No\n"
               "  Fully Charged           : Yes\n"
               "  Discharging             : No\n"
               "  Initialized             : No\n"
               "  Remaining Time Alarm    : Yes\n"
               "  Remaining Capacity Alarm: No\n"
               "  Discharge Terminated    : No\n"
               "  Over Temperature        : No\n"
               "  Charging Terminated     : No\n"
               "  Over Charged            : No\n\n"
               "Relative State of Charge: 92 %\n"
               "Charger Status: Complete\n"
               "Remaining Capacity: 540 mAh\n"
               "Full Charge Capacity: 593 mAh\n"
               "isSOHGood: Yes\n\n"
               "Exit Code: 0x00")
    assert_equals(scan_bbu(testtxt), {"bbu_nav": False,
                                      "bbu_charging": False,
                                      "bbu_ncharging": False})


def test_function_scan_bbu_not_available():
    testtxt = ("Exit Code: 0x10")
    assert_equals(scan_bbu(testtxt), {"bbu_nav": True,
                                      "bbu_charging": False,
                                      "bbu_ncharging": False})


def test_function_scan_physical_drive_predictive_errors():
    assert_equals(scan_physical_drive("Adapter #0\n\n"
                                      + "Enclosure Device ID: 32\n"
                                      + "Slot Number: 0\n"
                                      + "Enclosure position: 0\n"
                                      + "Device Id: 0\n"
                                      + "Sequence Number: 2\n"
                                      + "Media Error Count: 0\n"
                                      + "Other Error Count: 0\n"
                                      + "Predictive "
                                      + "Failure Count: 3\n"
                                      + "Last Predictive Failure "
                                      + "Event Seq Number: 0\n"
                                      + "PD Type: SATA\n"
                                      + "Raw Size: 93.160 GB "
                                      + "[0xba52230 Sectors]\n"
                                      + "Non Coerced Size: 92.660 "
                                      + "GB [0xb952230 Sectors]\n"
                                      + "Coerced Size: 92.625 GB "
                                      + "[0xb940000 Sectors]\n"
                                      + "Firmware state: Online, "
                                      + "Spun Up\n"
                                      + "SAS Address(0): "
                                      + "0x500056b37789abe3\n"
                                      + "Connected Port Number: "
                                      + "0(path0)\n"
                                      + "Inquiry Data:   "
                                      + "BTTV412301EN100FGNINTEL \n"
                                      + "SSDSC2BA100G3T\t5DV1DL05\n"
                                      + "FDE Capable: Not Capable\n"
                                      + "FDE Enable: Disable\n"
                                      + "Secured: Unsecured\n"
                                      + "Locked: Unlocked\n"
                                      + "Needs EKM Attention: No\n"
                                      + "Foreign State: None\n"
                                      + "Device Speed: 3.0Gb/s\n"
                                      + "Link Speed: 3.0Gb/s\n"
                                      + "Media Type: Solid State "
                                      + "Device\n"
                                      + "Drive Temperature :25C "
                                      + "(77.00 F)\n"),
                  (0, 0, 3, 0, 0))


def test_function_scan_physical_drive_hotsparecount():
    assert_equals(scan_physical_drive(("Adapter #0\n\n"
                                       "Enclosure Device ID: 32\n"
                                       "Slot Number: 0\n"
                                       "Enclosure position: 0\n"
                                       "Device Id: 0\n"
                                       "Sequence Number: 2\n"
                                       "Media Error Count: 0\n"
                                       "Other Error Count: 0\n"
                                       "Predictive "
                                       "Failure Count: 0\n"
                                       "Last Predictive Failure "
                                       "Event Seq Number: 0\n"
                                       "PD Type: SATA\n"
                                       "Raw Size: 93.160 GB "
                                       "[0xba52230 Sectors]\n"
                                       "Non Coerced Size: 92.660 "
                                       "GB [0xb952230 Sectors]\n"
                                       "Coerced Size: 92.625 GB "
                                       "[0xb940000 Sectors]\n"
                                       "Firmware state: Hotspare, "
                                       "Spun Up\n"
                                       "SAS Address(0): "
                                       "0x500056b37789abe3\n"
                                       "Connected Port Number: "
                                       "0(path0)\n"
                                       "Inquiry Data:   "
                                       "BTTV412301EN100FGNINTEL \n"
                                       "SSDSC2BA100G3T\t5DV1DL05\n"
                                       "FDE Capable: Not Capable\n"
                                       "FDE Enable: Disable\n"
                                       "Secured: Unsecured\n"
                                       "Locked: Unlocked\n"
                                       "Needs EKM Attention: No\n"
                                       "Foreign State: None\n"
                                       "Device Speed: 3.0Gb/s\n"
                                       "Link Speed: 3.0Gb/s\n"
                                       "Media Type: Solid State "
                                       "Device\n"
                                       "Drive Temperature :25C "
                                       "(77.00 F)\n")),

                  (0, 0, 0, 0, 1))


def test_function_scan_physical_drive_unknown_drive_status():
    with mock.patch('check_megaraid.sys.exit') as exit_mock:
        scan_physical_drive(("Adapter #0\n\n"
                             "Enclosure Device ID: 32\n"
                             "Slot Number: 0\n"
                             "Enclosure position: 0\n"
                             "Device Id: 0\n"
                             "Sequence Number: 2\n"
                             "Media Error Count: 0\n"
                             "Other Error Count: 0\n"
                             "Predictive "
                             "Failure Count: 0\n"
                             "Last Predictive Failure "
                             "Event Seq Number: 0\n"
                             "PD Type: SATA\n"
                             "Raw Size: 93.160 GB "
                             "[0xba52230 Sectors]\n"
                             "Non Coerced Size: 92.660 "
                             "GB [0xb952230 Sectors]\n"
                             "Coerced Size: 92.625 GB "
                             "[0xb940000 Sectors]\n"
                             "Firmware state: UnknownDriveStatus, "
                             "Spun Up\n"
                             "SAS Address(0): "
                             "0x500056b37789abe3\n"
                             "Connected Port Number: "
                             "0(path0)\n"
                             "Inquiry Data:   "
                             "BTTV412301EN100FGNINTEL \n"
                             "SSDSC2BA100G3T\t5DV1DL05\n"
                             "FDE Capable: Not Capable\n"
                             "FDE Enable: Disable\n"
                             "Secured: Unsecured\n"
                             "Locked: Unlocked\n"
                             "Needs EKM Attention: No\n"
                             "Foreign State: None\n"
                             "Device Speed: 3.0Gb/s\n"
                             "Link Speed: 3.0Gb/s\n"
                             "Media Type: Solid State "
                             "Device\n"
                             "Drive Temperature :25C "
                             "(77.00 F)\n"))
        assert exit_mock.called


def test_funtion_analyze_scanresult_missing_hotspare():
    scanresult = {
        "hotspare_count": 1,
        "logical_disk_count": 0,
        "physical_disk_count": 0,
        "media_errors": 0,
        "pred_errors": 0,
        "other_errors": 0,
        "physical_errors": 0,
        "logical_disk_errors": 0,
        "bbu_nav_count": 0,
        "bbu_charging_count": 0,
        "bbu_ncharging_count": 0}
    assert_equals(analyze_scanresult(scanresult, 0, 0, 0, 0, 0, 2),
                  (1, "Expected 2 Hotspares, got 1. (m0p0o0)"))


def test_funtion_analyze_scanresult_disk_errors():
    scanresult = {
        "hotspare_count": 0,
        "logical_disk_count": 0,
        "physical_disk_count": 0,
        "media_errors": 1,
        "pred_errors": 1,
        "other_errors": 1,
        "physical_errors": 0,
        "logical_disk_errors": 0,
        "bbu_nav_count": 0,
        "bbu_charging_count": 0,
        "bbu_ncharging_count": 0}
    assert_equals(analyze_scanresult(scanresult, 0, 0, 0, 0, 0, 0),
                  (1, "Found diskerrors. (m1p1o1)"))


def test_funtion_analyze_scanresult_disk_errors_ignore():
    scanresult = {
        "hotspare_count": 1,
        "logical_disk_count": 0,
        "physical_disk_count": 0,
        "media_errors": 1,
        "pred_errors": 1,
        "other_errors": 1,
        "physical_errors": 0,
        "logical_disk_errors": 0,
        "bbu_nav_count": 0,
        "bbu_charging_count": 0,
        "bbu_ncharging_count": 0}
    assert_equals(analyze_scanresult(scanresult, 0, 0, 1, 1, 1, 0),
                  (0, "Everything is ok. (m1p1o1)"))


def test_funtion_analyze_scanresult_physical_errors():
    scanresult = {
        "hotspare_count": 0,
        "logical_disk_count": 0,
        "physical_disk_count": 0,
        "media_errors": 0,
        "pred_errors": 0,
        "other_errors": 0,
        "physical_errors": 1,
        "logical_disk_errors": 0,
        "bbu_nav_count": 0,
        "bbu_charging_count": 0,
        "bbu_ncharging_count": 0}
    assert_equals(analyze_scanresult(scanresult, 0, 0, 0, 0, 0, 0),
                  (2, "Found 1 physical disk error(s). (m0p0o0)"))


def test_funtion_analyze_scanresult_logical_errors():
    scanresult = {
        "hotspare_count": 0,
        "logical_disk_count": 0,
        "physical_disk_count": 0,
        "media_errors": 0,
        "pred_errors": 0,
        "other_errors": 0,
        "physical_errors": 0,
        "logical_disk_errors": 2,
        "bbu_nav_count": 0,
        "bbu_charging_count": 0,
        "bbu_ncharging_count": 0}
    assert_equals(analyze_scanresult(scanresult, 0, 0, 0, 0, 0, 0),
                  (2, "Found 2 logical drive error(s). (m0p0o0)"))


def test_funtion_analyze_scanresult_bbu_nav():
    scanresult = {
        "hotspare_count": 0,
        "logical_disk_count": 0,
        "physical_disk_count": 0,
        "media_errors": 0,
        "pred_errors": 0,
        "other_errors": 0,
        "physical_errors": 0,
        "logical_disk_errors": 0,
        "bbu_nav_count": 1,
        "bbu_charging_count": 0,
        "bbu_ncharging_count": 0}
    assert_equals(analyze_scanresult(scanresult, 0, 0, 0, 0, 0, 0),
                  (2, "1 BBU not available. (m0p0o0)"))


def test_funtion_analyze_scanresult_bbu_charging():
    scanresult = {
        "hotspare_count": 0,
        "logical_disk_count": 0,
        "physical_disk_count": 0,
        "media_errors": 0,
        "pred_errors": 0,
        "other_errors": 0,
        "physical_errors": 0,
        "logical_disk_errors": 0,
        "bbu_nav_count": 0,
        "bbu_charging_count": 2,
        "bbu_ncharging_count": 0}
    assert_equals(analyze_scanresult(scanresult, 0, 0, 0, 0, 0, 0),
                  (1, "2 BBU charging. (m0p0o0)"))


def test_funtion_analyze_scanresult_bbu_not_charging():
    scanresult = {
        "hotspare_count": 0,
        "logical_disk_count": 0,
        "physical_disk_count": 0,
        "media_errors": 0,
        "pred_errors": 0,
        "other_errors": 0,
        "physical_errors": 0,
        "logical_disk_errors": 0,
        "bbu_nav_count": 0,
        "bbu_charging_count": 0,
        "bbu_ncharging_count": 3}
    assert_equals(analyze_scanresult(scanresult, 0, 0, 0, 0, 0, 0),
                  (1, "3 BBU not charging. (m0p0o0)"))


def test_funtion_analyze_scanresult_logical_disks():
    scanresult = {
        "hotspare_count": 0,
        "logical_disk_count": 1,
        "physical_disk_count": 0,
        "media_errors": 0,
        "pred_errors": 0,
        "other_errors": 0,
        "physical_errors": 0,
        "logical_disk_errors": 0,
        "bbu_nav_count": 0,
        "bbu_charging_count": 0,
        "bbu_ncharging_count": 0}
    assert_equals(analyze_scanresult(scanresult, 2, 0, 0, 0, 0, 0),
                  (2, "Missing logical Disk: Found 1 Expected 2. (m0p0o0)"))


def test_funtion_analyze_scanresult_all_together():
    scanresult = {
        "hotspare_count": 2,
        "logical_disk_count": 8,
        "physical_disk_count": 2,
        "media_errors": 1,
        "pred_errors": 1,
        "other_errors": 1,
        "physical_errors": 3,
        "logical_disk_errors": 2,
        "bbu_nav_count": 2,
        "bbu_charging_count": 3,
        "bbu_ncharging_count": 3}
    assert_equals(analyze_scanresult(scanresult, 9, 1, 0, 0, 0, 3),
                  (2, ("Missing logical Disk: Found 8 Expected 9. "
                       "Found 2 logical drive error(s). "
                       "Found 3 physical disk error(s). "
                       "2 BBU not available. "
                       "3 BBU not charging. "
                       "3 BBU charging. "
                       "Found diskerrors. "
                       "Expected 3 Hotspares, got 2. "
                       "(m1p1o1)")))


@mock.patch('check_megaraid.count_controller', return_value=2)
@mock.patch('check_megaraid.count_log_drives', return_value=1)
@mock.patch('check_megaraid.count_phys_drives', return_value=8)
@mock.patch('check_megaraid.execute', return_value=1)
@mock.patch('check_megaraid.scan_physical_drive',
            return_value=(1, 1, 1, 1, 1))
@mock.patch('check_megaraid.scan_logical_drive', return_value=1)
@mock.patch('check_megaraid.scan_bbu', return_value={"bbu_nav": 3,
                                                     "bbu_charging": 3,
                                                     "bbu_ncharging": 3})
def test_scan_controller(count_controller_function,
                         count_log_drives_function,
                         count_phys_drives_function,
                         execute_function,
                         scan_physical_drive_function,
                         scan_logical_drive_function,
                         scan_bbu_function):
    assert_equals(scan_controller(True),
                  {"logical_disk_errors": 2,
                   "media_errors": 2,
                   "logical_disk_count": 2,
                   "physical_disk_count": 16,
                   "other_errors": 2,
                   "pred_errors": 2,
                   "physical_errors": 2,
                   "hotspare_count": 2,
                   "bbu_nav_count": 6,
                   "bbu_charging_count": 6,
                   "bbu_ncharging_count": 6,
                   }
                  )


@mock.patch('check_megaraid.execute', return_value='Controller Count: 1.')
def test_count_controller(execute_function):
    assert_equals(count_controller(), 1)


@mock.patch('check_megaraid.execute', return_value='Just a wrong Sstring.')
def test_count_controller_failure(execute_function):
    assert_equals(count_controller(), 0)


@mock.patch('check_megaraid.execute',
            return_value=(('Number of Virtual Drives Configured'
                           ' on Adapter 0: 2')))
def test_count_log_drives(execut_function):
    assert_equals(count_log_drives(0), 2)


@mock.patch('check_megaraid.execute',
            return_value=(('Number of Physical Drives'
                           ' on Adapter 0: 2')))
def test_count_phys_drives(execut_function):
    assert_equals(count_phys_drives(0), 2)


@mock.patch('check_megaraid.execute',
            return_value='Just a wrong string')
def test_count_log_drives_failure(execut_function):
    assert_equals(count_log_drives(0), 0)
