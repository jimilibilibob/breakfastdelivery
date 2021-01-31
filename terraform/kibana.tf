resource "azurerm_public_ip" "kibana" {
    name                = "${var.env}-kibana-public-ip"
    location            = azurerm_resource_group.main.location
    resource_group_name = azurerm_resource_group.main.name
    allocation_method   = "Dynamic"
}

resource "azurerm_network_security_group" "kibana" {
    name                = "kibana-nsg"
    location            = azurerm_resource_group.main.location
    resource_group_name = azurerm_resource_group.main.name

    security_rule {
        name                       = "DenyAllInbound"
        priority                   = 666
        direction                  = "Inbound"
        access                     = "Allow"
        protocol                   = "Tcp"
        source_port_range          = "*"
        destination_port_range     = "*"
        source_address_prefix      = "*"
        destination_address_prefix = "*"
    }
    security_rule {
        name                       = "AllowInternetInbound"
        priority                   = 202
        direction                  = "Inbound"
        access                     = "Allow"
        protocol                   = "Tcp"
        source_port_range          = "*"
        destination_port_ranges    = ["5601"]
        source_address_prefix      = "*"
        destination_address_prefix = "*"
    }
    security_rule {
        name                       = "AllowAdminInbound"
        priority                   = 201
        direction                  = "Inbound"
        access                     = "Allow"
        protocol                   = "Tcp"
        source_port_range          = "*"
        destination_port_ranges    = ["22"]
        source_address_prefix      = "93.28.245.122"#"${chomp(data.http.ip.body)}"
        destination_address_prefix = "*"
    }
    security_rule {
        name                       = "AllowSnetInbound"
        priority                   = 200
        direction                  = "Inbound"
        access                     = "Allow"
        protocol                   = "Tcp"
        source_port_range          = "*"
        destination_port_range     = "*"
        source_address_prefixes    = azurerm_subnet.main.address_prefixes 
        destination_address_prefix = "*"
    }
}

resource "azurerm_network_interface" "kibana" {
    name                = "nic-${var.env}-kibana"
    location            = azurerm_resource_group.main.location
    resource_group_name = azurerm_resource_group.main.name

    ip_configuration {
        name                          = "ipconfig"
        subnet_id                     = azurerm_subnet.main.id
        private_ip_address_allocation = "Dynamic"
        public_ip_address_id          = azurerm_public_ip.kibana.id
    }
}

resource "azurerm_network_interface_security_group_association" "kibana" {
    network_interface_id      = azurerm_network_interface.kibana.id
    network_security_group_id = azurerm_network_security_group.kibana.id
}

resource "azurerm_linux_virtual_machine" "kibana" {
    name                = "kibana"
    resource_group_name = azurerm_resource_group.main.name
    location            = azurerm_resource_group.main.location
    size                = "Standard_D16_v4"
    admin_username      = var.admin_username 
    network_interface_ids = [
        azurerm_network_interface.kibana.id,
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

resource "azurerm_private_dns_a_record" "kibana" {
    name                = "kibana"
    zone_name           = azurerm_private_dns_zone.main.name
    resource_group_name = azurerm_resource_group.main.name
    ttl                 = 300
    records             = [azurerm_network_interface.kibana.private_ip_address]
}