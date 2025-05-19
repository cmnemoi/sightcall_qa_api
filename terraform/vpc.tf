resource "google_compute_network" "app_network" {
  name                    = "sightcall-qa-api-network"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "app_subnet" {
  name          = "sightcall-qa-api-subnet"
  ip_cidr_range = "10.8.0.0/28"
  region        = var.region
  network       = google_compute_network.app_network.id
}

resource "google_vpc_access_connector" "serverless_connector" {
  name          = "sightcall-qa-api-serverless-connector"
  region        = var.region
  network       = google_compute_network.app_network.name
  ip_cidr_range = "10.8.0.0/28"

  lifecycle {
    create_before_destroy = true
  }
}