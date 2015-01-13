import sys
import os
from os import listdir
from os.path import isfile, join
from optparse import OptionParser


parser = OptionParser()
parser.add_option("-t", "--tests", dest="tests_dir",
                  help="Directory holding tests", metavar="TESTSDIR" , default="./tests")
parser.add_option("-p", "--packetdrill", dest="packetdrill",
                  help="Packetdrill path", metavar="PACKETDRILL" , default=None)
parser.add_option("-s", "--sudo", dest="use_sudo",action="store_true",
                  help="Use sudo to run packetdrill scripts", metavar="USESUDO", default=True)
parser.add_option("-u", "--no-sudo", dest="use_sudo",action="store_false",
                  help="Use sudo to run packetdrill scripts", metavar="USESUDO")

(options, args) = parser.parse_args()

tests_dir=options.tests_dir.rstrip("/")

sys.path.insert(0,"lib")

import run_helpers as rh
from helpers import *

BaseTest.tests_dir=tests_dir
BaseTest.packetdrill=options.packetdrill
BaseTest.use_sudo=options.use_sudo
sys.path.insert(0,tests_dir)


if len(args)>0:
  # find tests based on arguments passed (filename of file name's prefix)
  test_names = [ rh.locate_test_file(tests_dir,f) for f in args ]
else:
  # no argument passed, run all tests
  test_names = [ f[:-3] for f in listdir(tests_dir) if isfile(join(tests_dir,f)) and f.endswith('.py')  ]
  test_names.sort()

for test_name in test_names:
  rh.run_test(test_name)
