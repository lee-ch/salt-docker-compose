path "secret/*" {
  capabilities = ["read", "list", "create", "update", "delete"]
}
 
path "auth/*" {
  capabilities = ["read", "list", "sudo", "create", "update", "delete"]
}
