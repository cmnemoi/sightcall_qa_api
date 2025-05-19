output "cloud_run_url" {
  value = google_cloud_run_service.fastapi.status[0].url
}

output "cloud_run_static_ip" {
  value       = google_compute_address.cloud_run_static_ip.address
  description = "Static IP used by Cloud Run through NAT"
}
