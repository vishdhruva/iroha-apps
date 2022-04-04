# TinyChain node class
import json
import docker
from os.path import exists

class TinyNode():
    client = docker.from_env()
    '''
        TinyChain node class
    '''
    def __init__(self, node_config = None):
        # Create a new node
        node_dict = {}
        if node_config == None:
            self.network = self.init_tinychain_network()
            self.postgres = self.init_postgres_container()
            self.blockstore = self.init_blockstore_volume()
            self.iroha = self.init_iroha_container()

            node_dict = {
                "network": self.network.name,
                "postgres": self.postgres.name,
                "blockstore": self.blockstore.name,
                "iroha": self.iroha.name
            }
            with open('config.json', 'w') as fp:
                json.dump(node_dict, fp)
        else: # Restart an existing node
            with open(node_config) as fp:
                node_dict = json.load(fp)
            self.network = self.client.networks.get(node_dict['network'])
            self.blockstore = self.client.volumes.get(node_dict['blockstore'])
            self.postgres = self.client.containers.get(node_dict['postgres'])
            self.iroha = self.client.containers.get(node_dict['iroha'])

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
        print("TinyChain blockstore created.")
        return blockstore

    def init_postgres_container(
            self,
            image='postgres:9.5',
            postgres_env = {
                'POSTGRES_USER': 'postgres',
                'POSTGRES_PASSWORD': 'mysecretpassword'
            },
            postgres_port = {'5432/tcp':5432}
        ):
        '''
            Initialize a postgres server.
        '''
        postgres = self.client.containers.create(
                image,
                name = 'tinychain-postgres',
                environment = postgres_env,
                ports = postgres_port,
                network = self.network.name,
                detach = True,
                cpu_shares = 100
            )
        print("Postgres container created")
        return postgres

    def init_iroha_container(
            self,
            iroha_image = 'hyperledger/iroha:latest',
            iroha_port = {'50051/tcp': 50051},
            configs_path = 'iroha/example', 
            container_path = '/opt/iroha_data',
        ):
        '''
            Initialize an iroha container
        '''
        iroha_container = self.client.containers.create(
            iroha_image,
            name = 'tinychain-iroha',
            ports = iroha_port,
            volumes = {
                configs_path: {
                    'bind': container_path,
                    'mode': 'rw'
                },
                self.blockstore.name: {
                    'bind': '/tmp/block_store',
                    'mode': 'rw'
                }
            },
            network = self.network.name
        )
        print("Iroha container created")
        return iroha_container

    def run(self):
        '''
            Run the Tinychain containers.
        '''
        self.postgres.start()
        self.iroha.start()

    def stop(self):
        '''
            Stop the Tinychain containers.
        '''
        self.iroha.stop()
        self.postgres.stop()

    def purge(self):
        '''
            Deletes the docker containers and instance of node. THIS IS IRREVERSIBLE.
        '''
        self.iroha.remove()
        self.blockstore.remove()
        self.postgres.remove()
        self.network.remove()
        with open('config.json', 'w') as fp:
            json.dump({}, fp)
        print('Volume, Network, and Container have been pruned')

        return

if __name__ == '__main__':
    node = None
    while (True):
        print("""Choose option: 
        1. Create node
        2. Load node
        3. Delete node
        4. Start node
        5. Stop node
        6. Exit""")
        option = input()
        if option == "1":
            if node != None:
                print('Node already exists. Please delete it first')
            node = TinyNode()
            print("created node")
        elif option == "2":
            if (exists('config.json')):
                node = TinyNode('config.json')
                print("Loaded node from config file")
            else:
                print("Config file not found")
        elif option == "3":
            if node == None:
                print("node is not loaded")
            else:
                node.purge()
                node = None
        elif option == "4":
            node.run()
            print("Node started successfully")
        elif option == "5":
            node.stop()
            print("Node stopped successfully")
        elif option == "6":
            break
        else:
            print("Invalid option\n")