variable "credentials_file_path" {
  description = "Path to GCP credentials file"
  default     = "./keys/my-creds.json"
}

variable "project" {
  description = "Project ID"
  default     = "zoomcamp-de-2026"
}

variable "location" {
  description = "Project location"
  default     = "EU"
}

variable "region" {
  description = "Project region"
  default     = "europe-central2"
}

variable "bq_dataset_name" {
  description = "My BigQuery dataset name"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "GCS Bucket Name"
  default     = "zoomcamp-de-2026-terraform-demo-bucket"
}

variable "gcs_storage_class" {
  description = "GCS Bucket Storage Class"
  default     = "STANDARD"
}