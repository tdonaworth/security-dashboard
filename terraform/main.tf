provider "aws" {
  profile = var.profile
  region  = var.region
}

data "aws_instance" "secbox" {
  //instance_id = "i-0f88b82116b9da827"

  filter {
    name = "tag:Name"
    values=["iQIES-SBX1-Centos-Security-Team"]
  }

  provisioner "remote-exec" {
    inline = [
      "sudo su -",
      "cd security-dashboard",
      "docker-compose down",
      "git pull",
      "docker-compose up -d"
    ]
  }
  
}

/*
resource "null_resource" "docker" {
    depends_on = ["aws_instance.security_box"]
    provisioner "local-exec" {
        command = "echo 'first'"
    }
}
*/

