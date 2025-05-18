variable "project_id" {
  type        = string
  description = "The ID of the GCP project"
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