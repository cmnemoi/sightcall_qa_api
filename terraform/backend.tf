terraform {
  backend "gcs" {
    bucket = "sightcall-qa-api-tfstate"
    prefix = "state/sightcall-qa-api"
  }
}
