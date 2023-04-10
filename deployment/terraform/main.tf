terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
    }
  }
}
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "tf_rg_def" {
  name     = "rgZoomCamp"
  location = var.region
}

resource "azurerm_storage_account" "tf_sa_def" {
  name                     = "emlak"
  resource_group_name      = azurerm_resource_group.tf_rg_def.name
  location                 = azurerm_resource_group.tf_rg_def.location
  account_tier             = var.storage_account_tier
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "tf_sa_cont_def" {
  name                  = "hepsiemlak"
  storage_account_name  = azurerm_storage_account.tf_sa_def.name
  container_access_type = "private"
}