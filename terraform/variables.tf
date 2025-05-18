variable "api_image_url" {
  type    = string
  default = "docker.io/cmnemoi/sightcall-qa-api:latest"
}

variable "cloud_run_env_vars" {
  type        = map(string)
  description = "Variables d'environnement pour Cloud Run"
  default     = {}
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
    "serviceusage.googleapis.com",
    "logging.googleapis.com",
    "monitoring.googleapis.com"
  ]
}

variable "project_id" {
  type        = string
  description = "The ID of the GCP project"
}

variable "region" {
  type    = string
  default = "europe-west1"
}