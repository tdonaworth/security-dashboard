// Global variables
variable "profile" {
  description = "AWS Profile to use, default is 'default'"
  default     = "default"
}

variable "region" {
  description = "AWS region"
  default     = "us-east-1"
}

variable "ami_id" {
  description = "The AMI to instantiate"
}

variable "security_group_ids" {
  description = "Main Security Groups"
  type        = list(string)
}

variable "instance_profile" {
  description = "The IAM Name for EC2 instances"
}

variable "dns_zone" {
  description = "The DNS Zone for the app"
}

variable "vpc_id" {
  description = "VPC ID"
}

variable "vpc_private_subnets" {
  description = "List of VPC private subnets"
  type        = list(string)
}

variable "ssl_arn" {
  description = "SSL certificate"
}

// Default variables

variable "vpc_cidr_block" {
  description = "VPC CIDR block"
  default     = "10.0.0.0/16"
}

variable "key_name" {
  description = "SSH KeyPair"
}