resource "azurerm_network_interface" "master" {
    name                = "nic-${var.env}-master"
    location            = azurerm_resource_group.main.location
    resource_group_name = azurerm_resource_group.main.name

    ip_configuration {
        name                          = "ipconfig"
        subnet_id                     = azurerm_subnet.main.id
        private_ip_address_allocation = "Dynamic"
    }
}

resource "azurerm_linux_virtual_machine" "master" {
    name                = "master-node"
    resource_group_name = azurerm_resource_group.main.name
    location            = azurerm_resource_group.main.location
    size                = "Standard_D2_v4"
    admin_username      = var.admin_username 
    network_interface_ids = [
        azurerm_network_interface.master.id,
    ]

    admin_ssh_key {
        username   = var.admin_username
        public_key = file(var.public_key)
    }

    os_disk {
        caching              = "ReadWrite"
        storage_account_type = "Standard_LRS"
    }

    source_image_reference {
        publisher = "Canonical"
        offer     = "UbuntuServer"
        sku       = "16.04-LTS"
        version   = "latest"
    }
}

resource "azurerm_private_dns_a_record" "master" {
    name                = "master"
    zone_name           = azurerm_private_dns_zone.main.name
    resource_group_name = azurerm_resource_group.main.name
    ttl                 = 300
    records             = [azurerm_network_interface.master.private_ip_address]
}