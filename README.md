# check_megaraid.py
a nagios plugin for checking the state of megaraid controller using MegaCli

This script checks the state of physical discs and logical volumes plugged at a
megaraidcontroller.
It is inspired by check_megaraid_sas 

usage: check_megaraid.py [-h] [-b] [-s SPARES] [-l LOGICAL] [-d DISKS]
                         [-m MEDIA] [-p PREDICTIVE] [-o OTHER] [--version]

nagios-check for megaraid-controllers

optional arguments:
  -h, --help            show this help message and exit
  -b, --bbu             check the bbu
  -s SPARES, --spares SPARES
                        expected number of hotspares at the controllers
  -l LOGICAL, --logical LOGICAL
                        expected number of logical disks at all controllers
  -d DISKS, --disks DISKS
                        expected number of physical disks at all controllers
  -m MEDIA, --media MEDIA
                        number of media errors to ignore
  -p PREDICTIVE, --predictive PREDICTIVE
                        number of predictiv errors to ignore
  -o OTHER, --other OTHER
                        number of other disk errors to ignore
  --version             show program's version number and exit

