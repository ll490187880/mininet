#!/usr/bin/python
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
def myNetwork():
    net = Mininet( topo=None,
                build=False,
                ipBase='10.0.0.0/8')
    info( '*** Adding controller\n' )
    c0=net.addController( name='c0',controller=RemoteController,
                          ip='20.0.1.3',
                          protocol='tcp',
                          port=6633)
#    info( '*** Add switches\n')
#    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
#    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
#    
#    info( '*** Add hosts\n')
#    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
#    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
#    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
#    
#    info( '*** Add links\n')
#    net.addLink(s1, h1)
#    net.addLink(s1, h2)
#    net.addLink(s1, s2)
#    net.addLink(s2, h3)
    L1 = 2
    L2 = L1 * 2 
    L3 = L2
    c = []
    a = []
    e = []
      
    # add core ovs  
    for i in range( L1 ):
            sw = net.addSwitch( 'c{}'.format( i + 1 ) )
            c.append( sw )

    # add aggregation ovs
    for i in range( L2 ):
            sw = net.addSwitch( 'a{}'.format( L1 + i + 1 ) )
            a.append( sw )

    # add edge ovs
    for i in range( L3 ):
            sw = net.addSwitch( 'e{}'.format( L1 + L2 + i + 1 ) )
            e.append( sw )

    # add links between core and aggregation ovs
    for i in range( L1 ):
            sw1 = c[i]
            for sw2 in a[i/2::L1/2]:
            # net.addLink(sw2, sw1, bw=10, delay='5ms', loss=10, max_queue_size=1000, use_htb=True)
	            net.addLink( sw2, sw1 )

    # add links between aggregation and edge ovs
    for i in range( 0, L2, 2 ):
            for sw1 in a[i:i+2]:
              for sw2 in e[i:i+2]:
	            net.addLink( sw2, sw1 )

    #add hosts and its links with edge ovs
    count = 1
    for sw1 in e:
            for i in range(2):
            	host = net.addHost( 'h{}'.format( count ) )
            	net.addLink( sw1, host )
            	count += 1
    
    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()
        
    info( '*** Starting switches\n')
    net.get('c').start([c0])
    net.get('a').start([c0])
    net.get('e').start([c0])
    
    info( '*** Post configure switches and hosts\n')
    CLI(net)
    net.stop()
if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
    
   
    
