variable "az" {
  description = "Availability zone for default environment"
  type = string 
  default = "us-east-1a"
}

variable "instance_type" {
  description = "Default instance type"
  type = string 
  default = "t3.micro"
}

variable "ebs_size" {
  description = "Default EBS size" 
  type = number
  default = 15
}

variable "lock" {
  description = "Locker"
  type = bool
}


