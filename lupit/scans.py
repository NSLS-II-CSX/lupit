from epicsscan import StepScan
import math
import numpy as np
import hashlib
import os
import time
import platform
import keyring
import pyOlog
import six
from dummyBroker import broker_commands

def frange(start,end=None,inc=None,p=None):
    if end == None:
        end = start + 0.
        start = 0.
    if inc == None:
        inc = 1.
    if p == None:
        p = 3
    if inc == 0:
        count = 1
    else:
        count = int(math.ceil( (end-start)/inc ))+1
    L = [None,] * count
    p = pow(10,p)

    start = start*p
    end = end*p
    inc = inc*p

    L[0] = float(start)/p
    for i in xrange(1,count):
        L[i] = L[i-1] + float(inc)/p

    return L

def prange(start, stop, nsteps):
    return np.linspace(start, stop, nsteps+1)


def get_unique_filename():
    h = hashlib.sha1('{0}{1}{2}'.format(time.time(), os.getlogin(),
                                        platform.node()))
    filename = '/epics/xf/23id/data/{0}.dat'.format(h.hexdigest())
    return filename


def scan(positioners=None, detectors=None,
         start=None, stop=None, step=1,
         dwelltime=None, scan_id=None,
         scan_description=None):
    """Scan macro

    positioners are a list of positioners to scan.
    detectors are a list of detetcors to measure for dwelltime

    Parameters
    ----------
    positioners : list
        List of pyepics positioners to scan
    detectors : list
        List of
    """
    # set some defaults
    if scan_id is None:
        scan_id = 1
    if dwelltime is None:
        dwelltime = 1
    if scan_description is None:
        scan_description = "scan"

    attributes = {}

    # convert input into lists
    try:
        iter(positioners)
    except TypeError:
        # raised if positioners is not iterable
        positioners = [positioners,]
    try:
        iter(detectors)
    except TypeError:
        # raised if detectors is not iterable
        detectors = [detectors,]
    try:
        iter(start)
    except TypeError:
        # raised if start is not iterable
        start = [start,]
    try:
        iter(stop)
    except TypeError:
        # raised if stop is not iterable
        stop = [stop,]

    # Now create the log entry for the olog

    # create some local methods

    def get_detector_data(detector):
        print('detector: {}'.format(detector))
        # print('counters:')
        data_dict = {}
        for counter in detector.counters:
            for name, val in six.iteritems(counter.get_buffers()):
                if len(val) > 0:
                    val = val[-1]
                data_dict[name] = val
                # print('\t{}, {}'.format(name, val))
        # print('data_dict: {}'.format(data_dict))
        return data_dict
        # return {name: val[-1] for counter in detector.counters
        #         for name,val in six.iteritems(counter.get_buffers())}

    def get_positioner_data(positioner):
        positioner_info = {positioner.pv.pvname: positioner.pv.get()}
        # print('positioner_info: {}'.format(positioner_info))
        return positioner_info

    def get_data_dict():
        data_dict = {}
        for positioner in positioners:
            data_dict.update(get_positioner_data(positioner))
        for detector in detectors:
            try:
                data_dict.update(get_detector_data(detector))
            except IndexError:
                detector.trigger.start()
                time.sleep(1)
                data_dict.update(get_detector_data(detector))
        return data_dict

    #username = os.getlogin()
    #c = pyOlog.OlogClient('https://xf23id-ca.cs.nsls2.local:8181/Olog',
    #                      username = username,
    #                      password = keyring.get_password('olog',username))

    # create the run header
    header = broker_commands.create_run_header(scan_id=scan_id)
    # create the event descriptor
    keys = get_data_dict()
    event_descriptor = broker_commands.create_event_descriptor(
        run_header=header, event_type_id=1, data_keys=keys,
        descriptor_name=scan_description)
    # write the header and event_descriptor to the header PV
    broker_commands.write_to_hdr_PV(header, event_descriptor)
    # create the pyepics step scan object
    s = StepScan()

    n = step + 1
    # set the instance attributes of the pyepics step scan
    [p.set_array(st,sp,n) for p,st,sp in zip(positioners, start, stop)]
    [s.add_detector(d) for d in detectors]
    [s.add_positioner(p) for p in positioners]

    # set a number of breakpoints equal to the number of steps in the scan
    s.breakpoints = range(n)

    # create the scan callback
    def scan_callback(breakpoint):
        """ Callback that gets executed at the end of each loop

        Parameters
        ----------
        loop_idx : int

        """
        scan_data = get_data_dict()
        print('all scan information: {}'.format(scan_data))
        # caget the detectors
        print('scan callback: {}'.format(breakpoint))
        event = broker_commands.format_event(header, event_descriptor,
                                              seq_no=breakpoint,
                                              data=scan_data)
        broker_commands.write_to_event_PV(event)

    # register a breakpoint function with the stepscan
    s.at_break_methods = [scan_callback,]

    s.set_dwelltime(dwelltime)

    filename = get_unique_filename()

    attributes['filename'] = filename

    scan_message    = 'Scan started at {0}\n'.format(time.asctime())
    scan_message += 'Filename : {0}\n\n'.format(filename)
    scan_message += 'Dwell Time : {0}\n\n'.format(dwelltime)
    scan_message += 'Positioners\n'
    scan_message += '===========\n'
    for p in positioners:
        scan_message += str(p) + '\n'
    scan_message += '\n'
    scan_message += 'Detectors\n'
    scan_message += '=========\n'
    for d in detectors:
        scan_message += str(d) + '\n'


    #c.log(pyOlog.LogEntry(scan_message, username,
    #                      logbooks = [pyOlog.Logbook('Commissioning',
    #                                  'swilkins')],
    #                      tags = [pyOlog.Tag('Autogenerated'),
    #                              pyOlog.Tag('Scan')]
    #                     )
    # )


    s.pos_settle_time = 1.0
    datafile = s.run(filename = get_unique_filename())

    print datafile

