output "kibana_public_ip" {
    value = azurerm_public_ip.kibana.ip_address
}

output "master_public_ip" {
    value = azurerm_public_ip.master.ip_address
}

output "master_private_ip" {
    value = azurerm_network_interface.master.private_ip_address
}

output "master_data_private_ip" {
    value = azurerm_network_interface.master_data.private_ip_address
}

output "data_private_ip" {
    value = azurerm_network_interface.data.private_ip_address
}