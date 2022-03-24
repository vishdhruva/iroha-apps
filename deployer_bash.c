//initial commands for docker curl and git install
sudo apt-get update
sudo apt install git-all
sudo apt-get install curl
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" 
apt-cache policy docker-ce
sudo apt-get install -y docker-ce
//docker network create
sudo docker network create tinychain-iroha-network

sudo docker run --name some-postgres \
-e POSTGRES_USER=postgres \
-e POSTGRES_PASSWORD=mysecretpassword \
-p 5432:5432 \
--network=srcmake-iroha-network \
-d postgres:9.5

sudo docker volume create blockstore

//git clone and running docker
git clone -b develop https://github.com/hyperledger/iroha --depth=1
sudo docker run -it --name iroha -p 50051:50051 -v $(pwd)/iroha/example:/opt/iroha_data -v blockstore:/tmp/block_store --network=tinychain-iroha-network --entrypoint=/bin/bash hyperledger/iroha:x86_64-develop-latest
irohad --config config.docker --genesis_block genesis.block --keypair_name node0

//interacting and launching the network
sudo docker exec -it iroha /bin/bash



