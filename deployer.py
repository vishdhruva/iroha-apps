import subprocess
def deployscript():
    while (True):
#initial install of docker and git 
        dockergitinstall = '''sudo apt-get update
        sudo apt install git-all
        sudo apt-get install curl
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
        sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" 
        apt-cache policy docker-ce
        sudo apt-get install -y docker-ce'''

        try:
            process = subprocess.run(dockergitinstall.split(), stdout=subprocess.PIPE)  
            output, error = process.stdout()
        except subprocess.CalledProcessError as e:  
            print(e.output)

#installation of docker network called tinychain

        dockernetwork = '''docker network create tinychain-iroha-network

        docker run --name some-postgres \
        -e POSTGRES_USER=postgres \
        -e POSTGRES_PASSWORD=mysecretpassword \
        -p 5432:5432 \
        --network=srcmake-iroha-network \
        -d postgres:9.5

        sudo docker volume create blockstore'''
        try:
            process = subprocess.run(dockernetwork.split(), stdout=subprocess.PIPE)
            output, error = process.stdout()
        except subprocess.CalledProcessError as e:
            print(e.output)

#cloning the git and installing docker

        gitclone = '''git clone -b develop https://github.com/hyperledger/iroha --depth=1
        docker run -it --name iroha -p 50051:50051 -v $(pwd)/iroha/example:/opt/iroha_data -v blockstore:/tmp/block_store --network=tinychain-iroha-network --entrypoint=/bin/bash hyperledger/iroha:x86_64-develop-latest
        irohad --config config.docker --genesis_block genesis.block --keypair_name node0'''

        try:
            process = subprocess.run(gitclone.split(), stdout=subprocess.PIPE)
            output, error = process.stdout()
        except subprocess.CalledProcessError as e:
            print(e.output)

def main():
    deployscript()







