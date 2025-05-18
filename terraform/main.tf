provider "google" {
  project = var.project_id
  region  = var.region
}

terraform {
  required_version = ">= 1.12"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.35"
    }
  }
}

resource "google_project_service" "enabled" {
  for_each           = toset(var.enabled_apis)
  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
}