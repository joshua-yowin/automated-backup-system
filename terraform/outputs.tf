output "resource_group_name" {
  value = azurerm_resource_group.backup_rg.name
}

output "storage_account_name" {
  value = azurerm_storage_account.backup_storage.name
}

output "container_name" {
  value = azurerm_storage_container.backup_container.name
}
