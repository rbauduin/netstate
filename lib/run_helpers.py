import sys
import glob
import os

# test_file is the import name of the test
def run_test(test_name):
  # import test file, and call functions in sequence
  current_test = __import__("%s"%test_name,globals(),locals(),[],0)
  current_test.Test(test_name).run()
  del sys.modules[test_name]

def locate_test_file(tests_dir, name):
  # import name, no change needed
  if os.path.isfile("%s/%s.py"%(tests_dir,name)):
    return name
  # file name, remove .py
  elif os.path.isfile("%s/%s"%(tests_dir,name)):
    return name[:-3]
  else:
    # prefix based. USeful to call test by number prefix:
    files = glob.glob("%s/%s*py"%(tests_dir,name))
    if len(files)==1:
      # remove "tests/"  and ".py"
      return files[0][len(tests_dir)+1:-3]

    # prefix based, but including the directory
    files = glob.glob("%s*py"%name)
    if len(files)==1:
      # remove "tests/"  and ".py"
      return files[0][len(tests_dir)+1:-3]
  raise "Test not found based on %s"%name  
  


