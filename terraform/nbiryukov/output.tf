output "instance_ip_addr" {
  value = aws_instance.aws_test_instance.private_ip
}

output "vpc_id" {
  value = module.vpc.vpc_id
}

