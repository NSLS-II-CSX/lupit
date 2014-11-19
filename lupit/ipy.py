import epicsscan

# Motors

slt3x  = epicsscan.Positioner('XF:23ID1-OP{Slt:3-Ax:X}Mtr')
slt3y  = epicsscan.Positioner('XF:23ID1-OP{Slt:3-Ax:Y}Mtr')
energy = epicsscan.Positioner('XF:23ID1-OP{Mono}Enrgy-SP', 
                              status_pvname = 'XF:23ID1-OP{Mono}Sts:Move-Sts')
epu1gap = epicsscan.Positioner('SR:C23-ID:G1A{EPU:1-Ax:Gap}-Mtr-SP',
                              status_pvname = 'SR:C23-ID:G1A{EPU:1-Ax:Gap}-Mtr.MOVN')
epu2gap = epicsscan.Positioner('SR:C23-ID:G1A{EPU:2-Ax:Gap}-Mtr-SP',
                              status_pvname = 'SR:C23-ID:G1A{EPU:2-Ax:Gap}-Mtr.MOVN')

# Detectors

sclr      = epicsscan.ScalerDetector('XF:23ID1-ES{Sclr:1}', use_calc=False)
esbeamcam = epicsscan.AreaDetector('XF:23ID1-ES{Dif-Cam:Beam}')
diag6cam  = epicsscan.AreaDetector('XF:23ID1-BI{Diag:6-Cam:1}')

# Counters

esbeamcam_stats1 = epicsscan.Counter('XF:23ID1-ES{Dif-Cam:Beam}Stats1:Total_RBV')
esbeamcam_stats2 = epicsscan.Counter('XF:23ID1-ES{Dif-Cam:Beam}Stats2:Total_RBV')
esbeamcam_stats3 = epicsscan.Counter('XF:23ID1-ES{Dif-Cam:Beam}Stats3:Total_RBV')
esbeamcam_stats4 = epicsscan.Counter('XF:23ID1-ES{Dif-Cam:Beam}Stats4:Total_RBV')
esbeamcam_stats5 = epicsscan.Counter('XF:23ID1-ES{Dif-Cam:Beam}Stats5:Total_RBV')

diag6cam_stats1 = epicsscan.Counter('XF:23ID1-BI{Diag:6-Cam:1}Stats1:Total_RBV')
diag6cam_stats2 = epicsscan.Counter('XF:23ID1-BI{Diag:6-Cam:1}Stats2:Total_RBV')
diag6cam_stats3 = epicsscan.Counter('XF:23ID1-BI{Diag:6-Cam:1}Stats3:Total_RBV')
diag6cam_stats4 = epicsscan.Counter('XF:23ID1-BI{Diag:6-Cam:1}Stats4:Total_RBV')
diag6cam_stats5 = epicsscan.Counter('XF:23ID1-BI{Diag:6-Cam:1}Stats5:Total_RBV')


def load_ipython_extension(ipython):
    print "Loaded scanit ipython extension"
    ipython.push('slt3x')
    ipython.push('slt3y')
    ipython.push('energy')
    ipython.push('sclr')
    ipython.push('esbeamcam')
    ipython.push('epu1gap')
    ipython.push('epu2gap')
    ipython.push('esbeamcam')
    ipython.push('diag6cam')
    ipython.push('diag6cam_stats1')
    ipython.push('diag6cam_stats2')
    ipython.push('diag6cam_stats3')
    ipython.push('diag6cam_stats4')
    ipython.push('diag6cam_stats5')
    ipython.push('esbeamcam_stats1')
    ipython.push('esbeamcam_stats2')
    ipython.push('esbeamcam_stats3')
    ipython.push('esbeamcam_stats4')
    ipython.push('esbeamcam_stats5')
