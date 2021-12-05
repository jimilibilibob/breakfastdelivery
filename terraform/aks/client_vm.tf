resource "azurerm_public_ip" "client" {
    name                = "${var.env}-client-public-ip"
    location            = azurerm_resource_group.main.location
    resource_group_name = azurerm_resource_group.main.name
    allocation_method   = "Dynamic"
}

resource "azurerm_network_interface" "client" {
    name                = "nic-${var.env}-client"
    location            = azurerm_resource_group.main.location
    resource_group_name = azurerm_resource_group.main.name

    ip_configuration {
        name                          = "ipconfig"
        subnet_id                     = azurerm_subnet.main.id
        private_ip_address_allocation = "Dynamic"
        public_ip_address_id          = azurerm_public_ip.client.id
    }
}

resource "random_password" "password" {
  length           = 16
  special          = true
  override_special = "_%@"
  min_lower   = 1
  min_numeric = 1
  min_special = 1
  min_upper   = 1
}

resource "azurerm_linux_virtual_machine" "client" {
    name                = "client"
    resource_group_name = azurerm_resource_group.main.name
    location            = azurerm_resource_group.main.location
    size                = "Standard_D2_v4"
    admin_username      = var.admin_username 
    network_interface_ids = [
        azurerm_network_interface.client.id,
    ]

    disable_password_authentication = false
    admin_password                  = random_password.password.result

    os_disk {
        caching              = "ReadWrite"
        storage_account_type = "Standard_LRS"
    }

    source_image_reference {
        publisher = "Canonical"
        offer     = "UbuntuServer"
        sku       = "18.04-LTS"
        version   = "latest"
    }
}

resource "null_resource" "config_file" {
    provisioner "file" {
        content     = azurerm_kubernetes_cluster.aks.kube_config_raw
        destination = "/tmp/config"
    }

    connection {
      type        = "ssh"
      host        = azurerm_linux_virtual_machine.client.public_ip_address
      user        = var.admin_username
      password    = random_password.password.result
      timeout     = "1m"
    }
}

resource "null_resource" "install_file" {
    provisioner "file" {
        source      = "files/install.sh"
        destination = "/tmp/install.sh"
    }

    connection {
      type        = "ssh"
      host        = azurerm_linux_virtual_machine.client.public_ip_address
      user        = var.admin_username
      password    = random_password.password.result
      timeout     = "1m"
    }
}

resource "null_resource" "client_install" {
    provisioner "remote-exec" {
        inline = [
        "chmod +x /tmp/install.sh",
        "/tmp/install.sh ${var.admin_username}",
        ]
    }

    connection {
      type        = "ssh"
      host        = azurerm_linux_virtual_machine.client.public_ip_address
      user        = var.admin_username
      password    = random_password.password.result
      timeout     = "1m"
    }

    depends_on = [
        null_resource.install_file,
        null_resource.config_file
    ]

}

resource "azurerm_network_security_group" "client" {
    name                = "client-nsg"
    location            = azurerm_resource_group.main.location
    resource_group_name = azurerm_resource_group.main.name

    security_rule {
        name                       = "AllowSSHInbound"
        priority                   = 200
        direction                  = "Inbound"
        access                     = "Allow"
        protocol                   = "Tcp"
        source_port_range          = "*"
        destination_port_range     = "22"
        source_address_prefix      = "*"
        destination_address_prefix = "*"
    }
}

resource "azurerm_network_interface_security_group_association" "client" {
    network_interface_id      = azurerm_network_interface.client.id
    network_security_group_id = azurerm_network_security_group.client.id
}