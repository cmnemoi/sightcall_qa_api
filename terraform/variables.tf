variable "project_name" {
  type        = string
  description = "The name of the GCP project"
}

variable "project_id" {
  type        = string
  description = "The ID of the GCP project"
}

variable "billing_account_id" {
  type        = string
  description = "The billing account ID to associate with the project"
}

variable "billing_user_email" {
  type        = string
  description = "The email of the user to grant billing permissions to"
}

variable "region" {
  type    = string
  default = "europe-west1"
}

variable "enabled_apis" {
  type = list(string)
  default = [
    "cloudresourcemanager.googleapis.com",
    "cloudbilling.googleapis.com",
    "compute.googleapis.com",
    "run.googleapis.com",
    "sqladmin.googleapis.com",
    "iam.googleapis.com",
    "secretmanager.googleapis.com",
    "serviceusage.googleapis.com",
    "logging.googleapis.com",
    "monitoring.googleapis.com"
  ]
}