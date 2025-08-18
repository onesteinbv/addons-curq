* Make empty record for s3 storage (use server_environment to complete it).

  In the odoo config file:
  ```
  [fs_storage.s3]
  protocol=s3
  options={"endpoint_url": "", "key": "", "secret": ""}
  directory_path=mybucket
  use_as_default_for_attachments=True
  use_filename_obfuscation=True
  ```
* Make sure all other files are in the database, so we don't need a separate volume (in k8s) for the filestore
*
