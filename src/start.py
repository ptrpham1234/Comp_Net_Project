from __future__ import print_function

import os
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel,info
from mininet.cli import CLI
from mininet.link import Intf
from mininet.node import Controller

class NetworkTopo(Topo):
	def build(self,**_opts):
		s1 = self.addSwitch('s1')
		h1 = self.addHost('h1')
		h2 = self.addHost('h2')
		h3 = self.addHost('h3')

		self.addLink(h1,s1)
		self.addLink(h2,s1)
		self.addLink(h3,s1)


def run():
	topo = NetworkTopo()

	net = Mininet(topo=topo)
	net.start()
	net['h1'].cmdPrint('python server.py &')
	net['h2'].cmdPrint('python render.py &')
	CLI(net)
	net.stop()

if __name__ == '__main__':
	setLogLevel('info')
	run()
