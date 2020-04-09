resource "aws_key_pair" "default" {
  key_name = "default"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC3rw3UV9m8iDpyz6olSnvVaTzJ4N4+4dHN7+7ipDhBo8Ka4Ye1uMhg8r56n+P+oYUdx5FffZE5kV6on5bFXhfl/wNoe+/6947MAdHuwU9ylVw0593vqzq2/MLHgJ55yOOlcZaUiBuNFIC0HI1JK8lXQLg2F4baUS64ZR3ba3DkaOo99Ocl3dyMxuSuGzDXUfORBQT3LHQjOViSRs+U63KdCuTjOQox7CLc0qAc51SOOpLUqWIY3ibK4hV05LkMukq6hBc7HSi7n7hi/b2ZE3GtCZ/fVVVlI37CZSGMDmABMji3pvXDuvAsLEZXCz+vWVeERcSojInFQ9FjN+64PmdIizrLikn8FXBP0H6uYaQ6vrEOHKewYy6as4w8nDfOYxqOZcU2Q33XTc/E3GCEM+DiMaByqQ9Vu8MYPaqO1zNu3YdafN9s1+6dH4KbadPKLvBt5YCR21lPEZ9o1DUVcBooauLk+Z0Rq+Itz1sQpO1rqk+Zg87jduec4UQGbmyKWo7Uu8mLwWXqxoHu8rFSDDhb3baJxYLYLTamjuJANhNBfLDxhyAzzMEuTCdoZ/N9Pt/0NR0BaQVNrAifygTQI6OZDKMDlh+2t+iSC0j5TNtVEvSGmjRHMps3N+U/UAxi+swsYouPlhRBVcjcgWY4Lk5R9xuC9Bi6dGoIbl3hc+EplQ== nbiryukov@csteer.pro"
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-trusty-14.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_instance" "aws_test_instance" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"
  availability_zone = var.az 
  key_name = aws_key_pair.default.id

  tags = {
    Name = "HelloWorld"
    Owner = "Nikolay Biryukov"
    Project = "TestProject"
  }
}

resource "aws_ebs_volume" "testEbs" {
  availability_zone = var.az
  size              = 10

  tags = {
    Name = "HelloWorld"
  }
}

resource "aws_volume_attachment" "ebs_att" {
  device_name = "/dev/sdh"
  volume_id   = aws_ebs_volume.testEbs.id
  instance_id = aws_instance.aws_test_instance.id
}
