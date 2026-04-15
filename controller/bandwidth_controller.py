from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class BandwidthController(object):
    def __init__(self, connection):
        self.connection = connection
        connection.addListeners(self)

    def _handle_PacketIn(self, event):
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        self.connection.send(msg)

def launch():
    def start_switch(event):
        log.info("Switch connected: %s", event.connection)
        BandwidthController(event.connection)

    core.openflow.addListenerByName("ConnectionUp", start_switch)


