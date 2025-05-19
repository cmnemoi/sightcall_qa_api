resource "google_sql_database_instance" "sql_instance_sightcall_qa_api" {
  name             = "sightcall-qa-api-db"
  region           = var.region
  database_version = "POSTGRES_17"

  settings {
    tier = "db-g1-small"

    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.app_network.self_link
    }

    database_flags {
      name  = "cloudsql.enable_pgvector"
      value = "on"
    }
  }

  deletion_protection = false
}

resource "google_sql_database" "vectordb" {
  name     = "sightcall_qa_api_vectordb"
  instance = google_sql_database_instance.sql_instance_sightcall_qa_api.name
}

resource "google_sql_user" "db_user" {
  name        = "sightcall_qa_api_user"
  instance    = google_sql_database_instance.sql_instance_sightcall_qa_api.name
  password_wo = var.db_password
}
