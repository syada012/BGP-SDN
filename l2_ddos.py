from pox.core import core
import pox.openflow.libopenflow_01 as of
from collections import Counter
import time

log = core.getLogger()

class LearningSwitch (object):
  MAX_REQUESTS = 20  # max requests allowed from a MAC address
  BLOCK_TIME = 60  # time in seconds to block a MAC address exceeding max requests

  def __init__ (self, connection):
    self.connection = connection
    self.mac_to_port = {}
    self.mac_counter = Counter()
    self.blocked_until = {}
    connection.addListeners(self)

  def resend_packet (self, packet_in, out_port):
    msg = of.ofp_packet_out()
    msg.data = packet_in
    action = of.ofp_action_output(port = out_port)
    msg.actions.append(action)
    self.connection.send(msg)

  def act_like_switch (self, packet, packet_in):
    mac = packet.src

    if mac in self.blocked_until and time.time() < self.blocked_until[mac]:
      log.warning(f"Blocked MAC {mac} tried to send packets.")
      return

    self.mac_to_port[mac] = packet_in.in_port
    self.mac_counter[mac] += 1

    if self.mac_counter[mac] > self.MAX_REQUESTS:
      self.blocked_until[mac] = time.time() + self.BLOCK_TIME
      log.warning(f"MAC {mac} has been blocked due to excessive requests.")
      self.mac_counter[mac] = 0
      return

    if packet.dst in self.mac_to_port:
      self.resend_packet(packet_in, self.mac_to_port[packet.dst])
    else:
      self.resend_packet(packet_in, of.OFPP_ALL)

  def _handle_PacketIn (self, event):
    packet = event.parsed
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp
    self.act_like_switch(packet, packet_in)

def launch ():
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    LearningSwitch(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)

