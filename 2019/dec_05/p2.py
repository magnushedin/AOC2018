""" Problem 5b - 2019 """

import ic
import sys

# For debugger to find the input
file_name = "./2019/dec_05/input_large_example"

if len(sys.argv) > 1:
    file_name = sys.argv[1]

my_ic = ic.Ic(file_name, 4)
my_ic.start_computer(0)
