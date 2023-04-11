FROM gitpod/workspace-full

RUN sudo apt-get update && sudo apt-get install -y apache2 php libapache2-mod-php php-mysql mysql-server
