#!/usr/bin/env bash

set -e
set -x

cd terraform

terraform fmt
terraform init
terraform plan
terraform apply
