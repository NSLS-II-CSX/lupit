__author__ = 'edill'

from lupit import scans
from lupit.ipy import *

positioners = [diag4y]

detectors = [sclr]

other_pvs = [energy, ]

scans.scan(positioners=positioners, detectors=detectors, start=6.7, stop=6.8,
           step=25, dwelltime=.1, scan_id=151, other_pvs=other_pvs)