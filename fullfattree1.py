
def simpleTest():
	"Create and test a simple network"
	topo = MyTopo()
	net = Mininet( topo, controller=RemoteController, host=CPULimitedHost, link=TCLink )
	net.addController( 'c0', controller=RemoteController, ip='20.0.1.3', port=6633 )
	net.start()
	print "Dumping host connections"
	dumpNodeConnections(net.hosts )
	print "Testing network connectivity"
	net.pingAll()
	print "Testing bandwidth between h1 with h2, h3, h5"
	h1, h2 = net.get( 'h1', 'h2' )
	net.iperf( ( h1, h2 ) )
	h1, h3 = net.get( 'h1', 'h3' )
	net.iperf( ( h1, h3 ) )
	h1, h5 = net.get( 'h1', 'h5' )
	net.iperf( ( h1, h5 ) )
	net.stop()
if __name__ == '__main__':
	# Tellmininet to print useful information
	setLogLevel( 'info' )
	simpleTest()
