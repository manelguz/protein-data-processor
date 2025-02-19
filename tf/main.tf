locals {
    workspace = terraform.workspace
    region = var.region
    account_id = data.aws_caller_identity.current.account_id
    ecr_address = format("%v.dkr.ecr.%v.amazonaws.com", local.account_id, local.region)
}

data "aws_caller_identity" "current" {}

terraform {
    required_version = "~> 1.7.3"

    backend "s3" {
        bucket = <bucket-name> # this must be replaced with your bucket name
        key    = "pdb.tfstate"
        region = "eu-west-1"
    }

    required_providers {
        aws = {
            source = "hashicorp/aws",
            version = "~> 5.37.0"
        }
        docker = {
            source  = "kreuzwerker/docker"
            version = ">= 2.8.0"
        }
    }
}

provider "aws" {
    region = local.region
}

data "aws_ecr_authorization_token" "token" {
  registry_id = aws_ecr_repository.pdb.registry_id
}

provider "docker" {
  registry_auth {
    address  = local.ecr_address
    username = data.aws_ecr_authorization_token.token.user_name
    password = data.aws_ecr_authorization_token.token.password
  }
}