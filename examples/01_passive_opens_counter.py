from helpers import *

class Test(BaseTest):
  def setup(self):
    self.counter_pre=get_counter("TcpPassiveOpens")
  def gen_traffic(self):
    self.packet_drilling()
  def validate(self):
    self.counter_post=get_counter("TcpPassiveOpens")
    assert(self.counter_post-self.counter_pre==1)
