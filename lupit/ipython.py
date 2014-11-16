import devices

slt3x = devices.ScanPositionerMotor('XF:23ID1-OP{Slt:3-Ax:X}Mtr')

def load_ipython_extension(ipython):
  print "Loaded scanit ipython extension"   
  ipython.push('slt3x')
