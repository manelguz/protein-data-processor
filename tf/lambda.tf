locals {
  repository_name = "manelguz/pdb"
}


resource "aws_ecr_repository" "pdb" {
  name                 = local.repository_name
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_lambda_function" "pdb" {
  function_name     = "${local.workspace}-pdb-backend"
  description       = "PDB backend for chan embedding calculation"

  package_type = "Image"
  image_uri = format("%v.dkr.ecr.%v.amazonaws.com/%v:%v",
    local.account_id,
    local.region,
    aws_ecr_repository.pdb.id,
    "latest"
  )
  source_code_hash = data.docker_registry_image.pdb.sha256_digest
  memory_size      = 3008 # common max limit in all regions
  timeout          = 30
  role             = aws_iam_role.pdb.arn

  image_config {
    command = ["handler.lambda_handler"]  
  }

  environment {
    variables = {
      "TORCH_HOME" = "/opt/ml/torch"
    }

  }

}


data "aws_iam_policy_document" "assume_pdb" {

  statement {
    actions = [
      "sts:AssumeRole",
    ]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    effect = "Allow"
  }

}

resource "aws_iam_role" "pdb" {
  name_prefix        = "pdb"
  assume_role_policy = data.aws_iam_policy_document.assume_pdb.json
}

resource "aws_iam_role_policy_attachment" "basic_pdb" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.pdb.name
}

data "docker_registry_image" "pdb" {
  name = docker_registry_image.pdb.name
}

resource "docker_registry_image" "pdb" {
  name = format("%v.dkr.ecr.%v.amazonaws.com/%v:%v",
    local.account_id,
    local.region,
    aws_ecr_repository.pdb.id,
    "latest"
  )
}