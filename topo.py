from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class NetworkTopo( Topo ):
    def build( self, **_opts ):

        s1, s2, s3 = [ self.addSwitch( s ) for s in ( 's1', 's2', 's3' ) ]

        h1 = self.addHost( 'h1', ip='10.0.0.1/16' )
        h5 = self.addHost( 'h5', ip='10.0.1.3/16' )

        # Adding links between switch and host
        self.addLink( s1, h1 )
        self.addLink( s3, h5 )

        # Adding links between switches
        self.addLink( s1, s2 )
        self.addLink( s2, s3 )

def run():
    topo = NetworkTopo()
    net = Mininet(topo=topo, controller=None, waitConnected=True)
    net.addController('c0', controller=RemoteController, ip="0.0.0.0", port=6633)
    net.start()

    # IP-based rules on switch 2
    # Assuming the outports are correct based on your topology
    net['s2'].cmd('ovs-ofctl add-flow s2 priority=1,ip,nw_dst=10.0.0.0/24,actions=output:1')
    net['s2'].cmd('ovs-ofctl add-flow s2 priority=1,ip,nw_dst=10.0.1.0/24,actions=output:2')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
