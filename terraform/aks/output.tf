output "vm_password" {
    value = random_password.password.result
}

output "vm_ip" {
    value = azurerm_linux_virtual_machine.client.public_ip_address
}

# output "kube_config" {
#   value = azurerm_kubernetes_cluster.aks.kube_config_raw
# }

output "kub_ingress_ip" {
  value = data.kubernetes_service.ingress_nginx.status.0.load_balancer.0.ingress.0.ip
}