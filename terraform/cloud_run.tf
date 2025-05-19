resource "google_service_account" "cloudrun_sa" {
  account_id   = "cloudrun-api"
  display_name = "Service Account for FastAPI on Cloud Run"
}

resource "google_cloud_run_service" "fastapi" {
  name     = "fastapi-api"
  location = var.region
  project  = var.project_id

  template {
    spec {
      service_account_name = google_service_account.cloudrun_sa.email

      containers {
        image = var.api_image_url

        ports {
          container_port = 3000
        }

        dynamic "env" {
          for_each = var.cloud_run_env_vars
          content {
            name  = env.key
            value = env.value
          }
        }
      }
    }

    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale" = "1"
        "autoscaling.knative.dev/maxScale" = "1"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

# Make API public
resource "google_cloud_run_service_iam_member" "public_invoker" {
  service  = google_cloud_run_service.fastapi.name
  location = var.region
  project  = var.project_id
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Map custom domain to Cloud Run service
resource "google_cloud_run_domain_mapping" "custom_domain" {
  location = var.region
  name     = var.api_url

  metadata {
    namespace = var.project_id
  }

  spec {
    route_name = "fastapi-api"
  }
}