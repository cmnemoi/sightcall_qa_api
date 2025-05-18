provider "google" {
  project = var.project_id
  region  = var.region
}

terraform {
  required_version = ">= 1.12"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.3"
    }
  }
}

resource "google_project" "project" {
  name       = var.project_name
  project_id = var.project_id
}

resource "google_project_service" "enabled" {
  for_each           = toset(var.enabled_apis)
  project            = google_project.project.project_id
  service            = each.value
  disable_on_destroy = false
}

resource "google_billing_account_iam_member" "billing_admin" {
  billing_account_id = var.billing_account_id
  role               = "roles/billing.admin"
  member             = "user:${var.billing_user_email}"
}

resource "google_billing_project_info" "billing" {
  project_id      = google_project.project.project_id
  billing_account = var.billing_account_id
}
