variable "subscription_id" {
    description = "Id de la souscription"
}

variable "location" {
    default = "francecentral"
    description = "location"
}

variable "env" {
    description = "Variable d'envrionnement"
}

variable "admin_username" {
    description = "admin username"
}

variable "public_key" {
    description = "public key"
    default = "~/.ssh/id_rsa.pub"
}

variable "ip"{
    default = "93.28.245.122"
}