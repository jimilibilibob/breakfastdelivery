resource "azurerm_kubernetes_cluster" "aks" {
  name                = "${var.env}-aks"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "${var.env}aks"

  kubernetes_version = "1.20.9"

  default_node_pool {
    name       = "default"
    node_count = 6
    vm_size    = "Standard_D4_v4"
  }

  identity {
    type = "SystemAssigned"
  }
}
