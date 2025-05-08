#!/usr/bin/env bash

set -e
set -x

cd terraform

terraform init
terraform plan
terraform apply
