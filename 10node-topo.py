#!/usr/bin/python

import re
from mininet.cli import CLI
from mininet.log import setLogLevel, info, error
from mininet.net import Mininet
from mininet.link import Intf
from mininet.topolib import TreeTopo
from mininet.util import quietRun
from mininet.node import RemoteController, OVSKernelSwitch, Controller

def checkIntf(intf):
    if(' %s:'% intf) not in quietRun('ip link show'):
        error('Error:', intf, 'can not exist\n' )
        exit(1)
    ips = re.findall( r'\d+\.\d+\.\d+\.\d+', quietRun( 'ifconfig ' + intf) )
    if ips:
        error('Error:', intf, 'has an IP address,'
            'and is probably in use!\n' )
        exit(1)

if __name__ =="__main__":
    setLogLevel("info")
    OVSKernelSwitch.setup()
    intfName_1 = "eth1" 
    intfName_3 = "eth2"
    info("***checking", intfName_1, '\n')
 #   checkIntf(intfName_1)
    info("***checking", intfName_3, '\n')
 #   checkIntf(intfName_3)

    info("***creating network\n")
    net = Mininet()
    
#    poxcontrol = RemoteController('poxcontrol', ip = '127.0.0.1')
    local1 = Controller( 'local1', port = 6634 )
#    local2 = Controller( 'local2', port = 6633 )

    sw_1 = net.addSwitch('s1')
    sw_2 = net.addSwitch('s2')
    sw_3 = net.addSwitch('s3')
    sw_4 = net.addSwitch('s4')
    sw_5 = net.addSwitch('s5')

    h1 = net.addHost('h1')
    h3 = net.addHost('h3')

#    net.controllers = [poxcontrol]
    
    net.addLink(sw_1, sw_2, 1, 1)
    net.addLink(sw_1, sw_5, 2, 1)
    net.addLink(sw_2, sw_5, 2, 2)
    net.addLink(sw_2, sw_3, 3, 1)
    net.addLink(sw_4, sw_5, 1, 3)
    net.addLink(sw_3, sw_4, 2, 2)
    net.addLink(sw_1, h1, port1 = 3)
    net.addLink(sw_3, h3, port1 = 3)

    info("***Adding hardware interface ", intfName_1, "to switch:", sw_1.name,'\n') 
    info("***Adding hardware interface ", intfName_3, "to switch:", sw_3.name,'\n')
    
    _intf_1 = Intf(intfName_1, node = sw_1, port = 3)
    _intf_3 = Intf(intfName_3, node = sw_3, port = 3)

    net.start()
#    local1.start()
 #   local2.start()
  #  sw_1.start(local1)
#    sw_2.start(local2)
#    sw_3.start(local1)
 #   sw_4.start(local2)
  #  sw_5.start(local1)

    CLI(net)
    net.stop()

