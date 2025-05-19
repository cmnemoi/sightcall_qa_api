resource "google_service_account" "cloudrun_sa" {
  account_id   = "cloudrun-api"
  display_name = "Service Account for FastAPI on Cloud Run"
}

resource "google_cloud_run_service" "fastapi" {
  name     = "sightcall-qa-api"
  location = var.region
  project  = var.project_id

  metadata {
    annotations = {
      "run.googleapis.com/cloudsql-instances"   = google_sql_database_instance.sql_instance_sightcall_qa_api.connection_name
      "run.googleapis.com/vpc-access-connector" = google_vpc_access_connector.serverless_connector.id
      "run.googleapis.com/vpc-access-egress"    = "all-traffic"
    }
  }

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

        env {
          name  = "DATABASE_URL"
          value = local.database_url
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
