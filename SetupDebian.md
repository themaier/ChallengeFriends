git, docker, docker-compose

sudo apt-get update
sudo apt-get install git -y

sudo apt-get update
sudo apt-get install \
 apt-transport-https \
 ca-certificates \
 curl \
 gnupg \
 lsb-release -y
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
 "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
 $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io -y

DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
mkdir -p $DOCKER_CONFIG/cli-plugins
curl -SL https://github.com/docker/compose/releases/download/v2.5.0/docker-compose-$(uname -s)-$(uname -m) -o $DOCKER_CONFIG/cli-plugins/docker-compose
chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose

git clone https://github.com/themaier/ChallengeFriends.git
cd ChallengeFriends
git checkout firebase-anonymous-login
cd frontend
touch .env
nano .env

sudo apt install nginx -y
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d norisknofun.life -d www.norisknofun.life

sudo mkdir -p ~/ssl #create an SSL directory to save the fullchain and privkey files

sudo cp -r -L /etc/letsencrypt/live/norisknofun.life/fullchain.pem ~/ChallengeFriends/frontend/nginx/
sudo cp -r -L /etc/letsencrypt/live/norisknofun.life/privkey.pem ~/ChallengeFriends/frontend/nginx/

sudo chown admin:admin ~/ChallengeFriends/frontend/nginx/fullchain.pem
sudo chown admin:admin ~/ChallengeFriends/frontend/nginx/privkey.pem

docker-compose -f docker-compose-production.yml up -d
