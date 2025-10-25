variable "resource_group_name" {
  description = "The name of the resource group."
  type        = string
  default     = "backup-rg"
}

variable "location" {
  description = "The Azure region where resources will be created."
  type        = string
  default     = "East US"
}

variable "storage_account_name" {
  description = "The name of the storage account."
  type        = string
  default     = "backupstorage123"
}

variable "container_name" {
  description = "The name of the storage container."
  type        = string
  default     = "backups"
}
