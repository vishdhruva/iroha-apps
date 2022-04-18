# TinyChain deployer
#
#
#
#

import subprocess
import sys
import pkg_resources
import docker

client = docker.from_env()

# initialize Docker network for TinyChain
def init_network():
    if 'tinychain-network' in client.networks.list():
        print("TinyChain network is already initialized on this node.")
    else:
        client.networks.create('tinychain-network')
        print("TinyChain network created.")
   

if __name__ == '__main__':
    init_network()