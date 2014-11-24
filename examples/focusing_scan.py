from lupit.ipy import *
from epics import caput
from lupit.scans import scan
exit_arm = epicsscan.Positioner('XF:23ID1-OP{Mono-Grt:01}Val:ExitArm-SP',
                                label='exitarm')
other_pvs = [exit_arm,]
positioners = [energy,]
detectors = [sclr,]
exit_arm_steps = range(12950, 13050, 10)
e_start = 454
e_stop = 458
e_step = int((458-454)/0.05)
e_dwelltime = 1

def scanit():
    for myy in exit_arm_steps:
        caput('XF:23ID1-OP{Mono-Grt:01}Val:ExitArm-SP', myy, wait=True)
        scan(positioners=positioners, detectors=detectors, start=e_start,
             stop=e_stop, step=e_step, dwelltime=e_dwelltime,
             other_pvs=other_pvs, scan_id=30)

if __name__ == '__main__':
    scanit()