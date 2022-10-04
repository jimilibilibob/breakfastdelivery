# helm repo add elastic https://helm.elastic.co
# helm repo add dsri https://maastrichtu-ids.github.io/dsri-helm-charts/

# helm repo update

RELEASE_NAME=practice
NAMESPACE=practice

# kubectl create namespace $NAMESPACE

# helm upgrade --install $RELEASE_NAME-elasticsearch elastic/elasticsearch \
#  -f ./kubernetes/examples/elasticsearch-values.yaml \
# --set clusterName=$RELEASE_NAME-elasticsearch \
# --version 7.11.1 \
# -n $NAMESPACE

# helm upgrade --install $RELEASE_NAME-kibana elastic/kibana \
#  -f ./kubernetes/examples/kibana-values.yaml \
# --set elasticsearchHosts=http://$RELEASE_NAME-elasticsearch-master:9200 \
# --version 7.11.1 \
# -n $NAMESPACE

# kubectl get all -n $NAMESPACE

# helm upgrade --install -n $NAMESPACE kafka-$RELEASE_NAME bitnami/kafka --set externalAccess.enabled=true --set externalAccess.autoDiscovery.enabled=true --set rbac.create=true


helm upgrade --install -n $NAMESPACE jupyterlab-$RELEASE_NAME dsri/jupyterlab \
  --set serviceAccount.name=jupyterlab \
  --set serviceAccount.sudoEnabled=false \
  --set serviceAccount.create=true \
  --set service.type=LoadBalancer \
  --set "podSecurityContext.supplementalGroups[0]=100" \
  --set service.openshiftRoute.enabled=false \
  --set image.repository=ghcr.io/maastrichtu-ids/jupyterlab \
  --set image.tag=latest \
  --set image.pullPolicy=Always \
  --set storage.mountPath=/home/jovyan/work \
  --set password=superTP2023