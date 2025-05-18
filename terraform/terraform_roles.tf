locals {
  terraform_roles = [
    "roles/run.admin",
    "roles/iam.serviceAccountUser",
    "roles/storage.admin"
  ]
}

resource "google_project_iam_member" "terraform_roles" {
  for_each = toset(local.terraform_roles)
  project  = var.project_id
  role     = each.value
  member   = "serviceAccount:${var.terraform_sa_email}"
}
