terraform {
    required_providers {
        azurerm = {
        source = "hashicorp/azurerm"
        version = ">= 2.26"
        }
    }
}

provider "azurerm" {
    subscription_id = var.subscription_id
    features {}
}

resource "azurerm_resource_group" "main" {
    name     = "${var.env}-elasticsearch-cluster-rg"
    location = var.location
}

resource "azurerm_virtual_network" "main" {
    name                = "${var.env}-vnet"
    address_space       = ["10.0.0.0/16"]
    location            = azurerm_resource_group.main.location
    resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_subnet" "main" {
    name                 = "${var.env}-snet"
    resource_group_name  = azurerm_resource_group.main.name
    virtual_network_name = azurerm_virtual_network.main.name
    address_prefixes     = ["10.0.0.0/24"]
}

resource "azurerm_private_dns_zone" "main" {
    name                = "elastic-cluster.com"
    resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_private_dns_zone_virtual_network_link" "main" {
    name                  = "clusterLink"
    resource_group_name   = azurerm_resource_group.main.name
    private_dns_zone_name = azurerm_private_dns_zone.main.name
    virtual_network_id    = azurerm_virtual_network.main.id
}