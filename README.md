# YGO Card Image Hosting

[![Documentation](https://img.shields.io/badge/Documentation-Link-blue)](https://nedhmn.github.io/ygo-card-image-hosting/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

This project provides an automated and efficient solution for downloading, archiving, and hosting Yu-Gi-Oh! card images using AWS S3 and CloudFront, managed with Terraform and a Dockerized Python script.

## ✨ Features

- **Automated AWS Infrastructure:** Sets up AWS S3 for storage and CloudFront for content delivery using **Terraform**.
- **Configurable Downloads:** Allows users to customize which card images are downloaded based on **date ranges** and image **sizes**.
- **Reliable CDN Delivery:** Serves your archived images globally with low latency via an AWS **CloudFront** Distribution.
- **Containerized Execution:** Runs the core logic within **Docker** for a consistent and portable environment.

## 🚀 Getting Started

This quickstart guide will help you get `ygo-card-image-hosting` up and running to archive and serve card images.

### Prerequisites

You will need the following installed on your machine:

- An **AWS Account** with configured credentials.
- **Terraform**
- **Docker** and **Docker Compose**

Refer to the **[Installation section in the documentation](https://nedhmn.github.io/ygo-card-image-hosting/getting-started/installation/)** for detailed instructions on installing prerequisites.

### Clone the Repository

```bash
git clone https://github.com/nedhmn/ygo-card-image-hosting.git
cd ygo-card-image-hosting
```

### Configure Your Environment

You need to create and configure two files: `.auto.tfvars` for Terraform and `.env` for the application.

1.  **Create `./terraform/.auto.tfvars`:** <br><br>
    Navigate to the `./terraform` directory and create a file named `.auto.tfvars`. Add your AWS credentials and desired S3 bucket name:

    ```hcl
    aws_region            = "your-aws-region"
    aws_access_key_id     = "your-access-key-id"
    aws_secret_access_key = "your-secret-access-key"
    bucket_name           = "your-unique-bucket-name" # Must be globally unique
    ```

2.  **Create `./.env`:**<br><br>
    Navigate back to the project root and create a file named `.env`. Copy the content from `.env.example` and fill in your AWS credentials and optional download configuration:

    ```dotenv
    # YGOPRODECK
    START_DATE=
    END_DATE=
    DATE_REGION=
    CARD_SIZE=

    # AWS
    AWS_REGION=
    AWS_ACCESS_KEY_ID=
    AWS_SECRET_ACCESS_KEY=
    BUCKET_NAME=
    ```

Refer to the **[Configuration section in the documentation](https://nedhmn.github.io/ygo-card-image-hosting/getting-started/configuration/)** for detailed instructions on all configuration options.

### Run the Hosting Service

1.  **Set up AWS Infrastructure:**
    From the project root, run the Terraform script to provision your AWS resources:

    ```bash
    bash scripts/run_terraform.sh
    ```

    Follow the prompts. Note that CloudFront setup can take up to 15 minutes. The CloudFront hostname will be printed upon completion - **save this hostname**.

2.  **Run the Image Archiving Script:**
    From the project root, build and run the Docker container:

    ```bash
    docker compose up --build
    ```

    The script will download and upload images. It will skip images already present in S3.

For more detailed information on running the service and verifying the setup, refer to the **[Running the Hosting Service section in the documentation](https://nedhmn.github.io/ygo-card-image-hosting/getting-started/running-the-project/)**.

## 📖 Documentation

Explore the full documentation for detailed guides on configuration, running the service, customizing downloads, and serving images for specific formats:

**[https://nedhmn.github.io/ygo-card-image-hosting/](https://nedhmn.github.io/ygo-card-image-hosting/)**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
