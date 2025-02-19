data "template_file" "api" {
  template = file("${path.module}/api.yml")
  vars = {
    get_embedding_arn = aws_lambda_function.pdb.invoke_arn
  }
}

resource "aws_api_gateway_rest_api" "api" {
  name        = "pdb-api-${local.workspace}"
  description = "The PDB API"
  body        = data.template_file.api.rendered
}

# deployment
resource "aws_api_gateway_deployment" "pdb" {
  rest_api_id = aws_api_gateway_rest_api.api.id

  triggers = {
    redeployment = sha1(data.template_file.api.rendered)
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_lambda_permission" "lambda_permissions" {

  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.pdb.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn    = "${aws_api_gateway_rest_api.api.execution_arn}/*/POST/get_embeddings"
}


//Api logging
resource "aws_api_gateway_account" "pdb_api" {
  cloudwatch_role_arn = aws_iam_role.pdb_api.arn
}

resource "aws_iam_role" "pdb_api" {
  name_prefix        = "${local.workspace}-pdb-api"
  assume_role_policy = data.aws_iam_policy_document.assume_api.json
}

data "aws_iam_policy_document" "assume_api" {
  statement {
    actions = [
      "sts:AssumeRole",
    ]

    principals {
      type        = "Service"
      identifiers = ["apigateway.amazonaws.com"]
    }

    effect = "Allow"
  }
}

resource "aws_iam_role_policy_attachment" "main" {
  role       = aws_iam_role.pdb_api.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs"
}

resource "aws_api_gateway_method_settings" "pdb_api_settings" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  stage_name  = aws_api_gateway_stage.stage.stage_name
  method_path = "*/*"
  settings {
    logging_level = "INFO"
    data_trace_enabled = true
    metrics_enabled = true
  }

  depends_on = [ aws_api_gateway_account.pdb_api ]
}

//API STAGE
resource "aws_api_gateway_stage" "stage" {
  deployment_id = aws_api_gateway_deployment.pdb.id
  rest_api_id   = aws_api_gateway_rest_api.api.id
  stage_name    = local.workspace
}
