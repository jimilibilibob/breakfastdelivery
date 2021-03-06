#!/bin/sh
wget https://get.helm.sh/helm-v3.5.2-linux-amd64.tar.gz
tar -zxvf helm-v3.5.2-linux-amd64.tar.gz
mv linux-amd64/helm ~/helm
rm -rf helm-v3.5.2-linux-amd64.tar.gz
rm -rf linux-amd64