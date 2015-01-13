
import os
import sys,traceback
import subprocess

def get_counter(counter):
  out=subprocess.check_output(["nstat", "-az",counter])
  if len(out.split("\n"))>2:
    return int(str(out).split()[2])
  else:
    return 0

class IncrementException(Exception):
  def __init__(self,expect, pre, post, title):
    self.message="Expected increment of %i in %s, but got %i (from %i to %i)"%(expect,title,post-pre,pre,post)

def assert_increment(expected, pre, post, title):
  """ Asserts that post-pre==expected, and raises an IncrementException otherwise.
      The title argument should identify the assertion that is tested.
  """
  if post-pre!=expected:
    raise IncrementException(expected, pre, post, title)

class BaseTest():
  def __init__(self,test_name):
    # name of test, is the import name
    self.name=test_name
    # tests directory, set base class in run.py
    self.tests_dir = BaseTest.tests_dir
    self.packetdrill = BaseTest.packetdrill
    self.use_sudo  = BaseTest.use_sudo
  def run(self):
    try:
      step="setup"
      self.setup()
      step="gen_traffic"
      self.gen_traffic()
      step="validate"
      self.validate()
      step="cleanup"
      self.cleanup()
    except AssertionError as e:
      _,_,tb = sys.exc_info()
      tbInfo = traceback.extract_tb(tb)
      filename,line,func,text = tbInfo[-1]
      print ('An error occurred '+ filename + '#' + str(line) + ' in statement:\n ' + text)
      print (e.args[0])
      exit(1)
    except Exception as err:
      _,_,tb = sys.exc_info()
      tbInfo = traceback.extract_tb(tb)
      filename,line,func,text = tbInfo[-1]
      print("An error occured in step %s:"%(step))
      print(err.message)
      # this should extract the line in the test file where the error occured
      error_line=traceback.format_exc().splitlines()[3]
      print(error_line)
      exit(1)
  def packet_drilling(self,fname=None):
    # raise error if not found
    if fname==None and not os.path.isfile("%s/%s.drill"%(self.tests_dir,self.name)):
      raise BaseException("Packetdrill file not found (%s/%s.drill)"%(self.tests_dir,self.name))

    if fname==None:
      filename="%s/%s.drill"%(self.tests_dir,self.name)
    else:
      filename=fname
    try:
      cmd=[self.packetdrill,filename]
      if self.use_sudo:
        cmd.insert(0,"sudo")
      status = subprocess.check_output(cmd,stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
      print("Packet drill error:")
      print(err.output)
      raise err
  def setup(self):
    pass
  def gen_traffic(self):
    self.packet_drilling()
  def validate(self):
    pass
  def cleanup(self):
    pass
