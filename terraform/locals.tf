locals {
  database_url = format(
    "postgresql://%s:%s@/%s?host=/cloudsql/%s",
    google_sql_user.db_user.name,
    var.db_password,
    google_sql_database.vectordb.name,
    google_sql_database_instance.sql_instance_sightcall_qa_api.connection_name
  )
}
