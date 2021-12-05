#!/bin/bash

echo "Running apt update" > /tmp/install.log
sudo apt-get update

echo "Install python3-pi" >> /tmp/install.log
sudo apt-get install python3-pip -y

echo "Download Kubectl 1.20" >> /tmp/install.log
curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.20.0/bin/linux/amd64/kubectl

echo "Install Kubectl" >> /tmp/install.log
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl

echo "Test Kubectl" >> /tmp/install.log
kubectl version --client >> /tmp/install.log

admin_username=$1
echo "Config user $1">> /tmp/install.log

echo "Test Kubectl Config" >> /tmp/install.log
mkdir /home/$admin_username/.kube
cp /tmp/config /home/$admin_username/.kube/config
chmod go-r /home/$admin_username/.kube/config
kubectl version --client >> /tmp/install.log

echo "Install Helm" >> /tmp/install.log
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
rm ./get_helm.sh

echo "Test helm" >> /tmp/install.log
helm version >> /tmp/install.log