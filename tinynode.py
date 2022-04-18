# TinyChain node class
import docker
import json

class TinyNode():
    client = docker.from_env()
    '''
        Initialize a tinychain node.
    '''
    def __init__(self, config = None):
        # Create a new node
        if config == None:
            self.network = self.init_tinychain_network()
            self.postgres = self.init_postgres_container()
            self.blockstore = self.init_blockstore_volume()
        # Restart an existing node
        else:
            pass

        
    def init_tinychain_network(self):
        '''
            Initialize a docker network.
        '''
        network = self.client.networks.create('tinychain-network')
        print("TinyChain network created.")
        return network
    
    def init_blockstore_volume(self):
        ''' 
            initialize blockstore
        '''
        blockstore = self.client.volumes.create('tinychain-blockstore')
        print("Blockstore created.")
        return blockstore

    def init_postgres_container(self):
        '''
            Initialize a postgres server.
        '''


    def init_iroha_container(
        self,
        iroha_image = 'hyperledger/iroha:latest',
        iroha_port = {'50051/tcp': 50051},
        configs_path = '$(pwd)/iroha/example', 
        container_path = '/opt/iroha_data',
        node_name = 'node0'
    ):
        '''
            Initialize an iroha container
        '''
        iroha_container = self.client.containers.create(
            iroha_image,
            name = 'tinychain-iroha',
            ports = iroha_port,
            volumes = {
                configs_path: container_path,
                self.blockstore.name(): '/tmp/block_store'
            },
            network = self.network.name(),
            environment = { 'KEY': node_name },
        )
        print("Iroha container created")
        return iroha_container

    def init_purge(self):
        '''
            Deletes all docker containers and instance of node. THIS IS IRREVERSIBLE.
        '''
        prune_block= self.client.api.prune_volumes(blockstore=self)
        prune_net = self.client.api.prune_networks(network=self)
        prune_container = self.client.api.prune_containers(iroha_container=self)
        print('Volume, Network, and Container have been pruned')
        pass

    def status_volume(self):
        '''
            Checks volume data
        '''
        status = self.client.api.inspect_volume(blockstore = self)
        print('Status of Volume Retrieved')
        return status 