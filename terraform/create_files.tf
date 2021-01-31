resource "local_file" "ssh" {
    content     = <<EOF
Host kibana
 Hostname ${azurerm_public_ip.kibana.ip_address}
 User administrateur
 IdentityFile ~/.ssh/id_rsa

Host *.elastic-cluster.com
 ProxyCommand ssh -F ssh.cfg -W %h:%p kibana
 User administrateur
 IdentityFile ~/.ssh/id_rsa

Host *
 ControlMaster   auto
 ControlPath     ~/.ssh/mux-%r@%h:%p
 ControlPersist  15m
EOF
    filename = "file/ssh.cfg"
}

resource "local_file" "inventory" {
    content     = <<EOF
all:
    children:
        master:
            hosts:
                master.elastic-cluster.com:
        master-data:
            hosts:
                master-data.elastic-cluster.com:
        data:
            hosts:
                data.elastic-cluster.com:
        kibana:
            hosts:
                ${azurerm_public_ip.kibana.ip_address}:
EOF
    filename = "file/inventory.yml"
}