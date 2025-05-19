# -----------------------------------------------------------------------------
# VPC Configuration for Cloud Run Egress via NAT
# -----------------------------------------------------------------------------

# Creates a custom VPC network (no auto subnet creation)
resource "google_compute_network" "run_vpc" {
  name                    = "sightcall-qa-api-vpc"
  auto_create_subnetworks = false
}

# Subnet used specifically for the Serverless VPC Access Connector
resource "google_compute_subnetwork" "run_subnet" {
  name          = "sightcall-qa-api-subnet"
  ip_cidr_range = "10.10.20.0/28"
  region        = var.region
  network       = google_compute_network.run_vpc.id
}

# -----------------------------------------------------------------------------
# Serverless VPC Access Connector
# -----------------------------------------------------------------------------

# Enables Cloud Run to access resources in the VPC
resource "google_vpc_access_connector" "run_connector" {
  name           = "scqa-connector"
  region         = var.region
  network        = google_compute_network.run_vpc.name
  ip_cidr_range  = "10.10.21.0/28"
  min_throughput = 200
  max_throughput = 300

  lifecycle {
    create_before_destroy = true
  }
}

# -----------------------------------------------------------------------------
# Static IP Address and NAT Configuration
# -----------------------------------------------------------------------------

# Reserves a static external IP address for outbound traffic
resource "google_compute_address" "cloud_run_static_ip" {
  name   = "sightcall-qa-api-static-ip"
  region = var.region
}

# Creates a Cloud Router to support Cloud NAT
resource "google_compute_router" "run_router" {
  name    = "sightcall-qa-api-router"
  region  = var.region
  network = google_compute_network.run_vpc.id
}

# Configures Cloud NAT to route egress traffic through the static IP
resource "google_compute_router_nat" "run_nat" {
  name   = "sightcall-qa-api-nat"
  router = google_compute_router.run_router.name
  region = var.region

  # Manually assign our reserved static IP
  nat_ip_allocate_option = "MANUAL_ONLY"
  nat_ips                = [google_compute_address.cloud_run_static_ip.id]

  # Apply NAT to all subnetworks and IP ranges in the VPC
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"
}
