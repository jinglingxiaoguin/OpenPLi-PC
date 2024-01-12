#!/bin/sh

# This is a script for automatically reinstall all packages from the dpkg list.
# Very useful in case of hhd / ssd have bad sectors or other emergencies.
# You only need to press "enter" and drink beer.

yes  | (for p in `dpkg -l|egrep '^ii'|awk '{print $2}'`; do apt-get install --reinstall $p ; done)


