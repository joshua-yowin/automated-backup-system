provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "backup_rg" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_storage_account" "backup_storage" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.backup_rg.name
  location                 = azurerm_resource_group.backup_rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "backup_container" {
  name                  = var.container_name
  storage_account_name  = azurerm_storage_account.backup_storage.name
  container_access_type = "private"
}
