import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/aklile/Desktop/MR_Exercise1-/ex_ws/install/turtlesim_pde4430'
