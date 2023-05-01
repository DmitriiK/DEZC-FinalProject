
variable "region" {
  description = "Region for Azure resources. "
  default = "West Europe"
  type = string
}

variable "storage_account_tier" {
  description = "Storage account_tier."
  default = "Standard"
}