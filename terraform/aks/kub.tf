provider "kubernetes" {
  host                   = azurerm_kubernetes_cluster.aks.kube_config.0.host
  username               = azurerm_kubernetes_cluster.aks.kube_config.0.username
  password               = azurerm_kubernetes_cluster.aks.kube_config.0.password
  client_certificate     = base64decode(azurerm_kubernetes_cluster.aks.kube_config.0.client_certificate)
  client_key             = base64decode(azurerm_kubernetes_cluster.aks.kube_config.0.client_key)
  cluster_ca_certificate = base64decode(azurerm_kubernetes_cluster.aks.kube_config.0.cluster_ca_certificate)
}

provider "helm" {
  kubernetes {
    host                   = azurerm_kubernetes_cluster.aks.kube_config.0.host
    username               = azurerm_kubernetes_cluster.aks.kube_config.0.username
    password               = azurerm_kubernetes_cluster.aks.kube_config.0.password
    client_certificate     = base64decode(azurerm_kubernetes_cluster.aks.kube_config.0.client_certificate)
    client_key             = base64decode(azurerm_kubernetes_cluster.aks.kube_config.0.client_key)
    cluster_ca_certificate = base64decode(azurerm_kubernetes_cluster.aks.kube_config.0.cluster_ca_certificate)
  }
}

resource "kubernetes_namespace" "ingress_nginx" {
  metadata {
    annotations = {
      name = "ingress-nginx"
    }

    name = "ingress-nginx"
  }

  depends_on = [
    azurerm_kubernetes_cluster.aks
  ]
}

resource "helm_release" "ingress_nginx" {
  name       = "ingress-nginx"

  repository = "https://kubernetes.github.io/ingress-nginx"
  chart      = "ingress-nginx"

  namespace = "ingress-nginx"

  depends_on = [
    kubernetes_namespace.ingress_nginx
  ]
}

data "kubernetes_service" "ingress_nginx" {
  metadata {
    name = "ingress-nginx-controller"
    namespace = "ingress-nginx"
  }

  depends_on = [
    helm_release.ingress_nginx
  ]
}