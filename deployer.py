import subprocess
def initializeiroha():
    while (True):
#initial install of docker and git 
        dockergitcloneinstall = '''sudo apt-get update
        sudo apt install git-all
        sudo apt-get install curl
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
        sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" 
        
        apt-cache policy docker-ce

        sudo apt-get install -y docker-ce

        git clone -b develop https://github.com/hyperledger/iroha --depth=1
        sudo docker run -it --name iroha -p 50051:50051 -v $(pwd)/iroha/example:/opt/iroha_data -v blockstore:/tmp/block_store --network=tinychain-iroha-network --entrypoint=/bin/bash hyperledger/iroha:x86_64-develop-latest
        irohad --config config.docker --genesis_block genesis.block --keypair_name node0
        '''
        try:
            process = subprocess.run(dockergitcloneinstall.split(), stdout=subprocess.PIPE)  
            output, error = process.stdout()
        except subprocess.CalledProcessError as e:  
            print(e.output)
def net_initialize():
#installation of docker network called tinychain
        dockernetwork = '''docker network create tinychain-iroha-network
        
        docker run --name some-postgres \
        -e POSTGRES_USER=postgres \
        -e POSTGRES_PASSWORD=mysecretpassword \
        -p 5432:5432 \
        --network=tinychain-iroha-network \
        -d postgres:9.5'''

        try:
            process = subprocess.run(dockernetwork.split(), stdout=subprocess.PIPE)
            output, error = process.stdout()
        except subprocess.CalledProcessError as e:
            print(e.output)


def start_up():
#start of of postgres and docker
        iroha_create = '''docker start post-gres

        docker volume create blockstore'''

        try:
            process = subprocess.run(iroha_create.split(), stdout=subprocess.PIPE)
            output, error = process.stdout()
        except subprocess.CalledProcessError as e:
            print(e.output)

def main():
    initializeiroha()
    net_initialize()
    start_up()







