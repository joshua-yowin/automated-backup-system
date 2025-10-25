# Azure Deployment Guide

This guide details the steps for deploying Azure resources and integrating with the backup system.

## 1. Login to Azure

Ensure you are logged into your Azure account using the Azure CLI:

```bash
az login
```

Follow the on-screen instructions to complete the login process.

## 2. Create Service Principal for Jenkins

Create an Azure Service Principal that Jenkins will use to authenticate and manage Azure resources. This service principal needs `Contributor` role access to your subscription.

```bash
az ad sp create-for-rbac --name "jenkins-backup" \
  --role="Contributor" \
  --scopes="/subscriptions/<YOUR_SUBSCRIPTION_ID>"
```

**Important:** Replace `<YOUR_SUBSCRIPTION_ID>` with your actual Azure subscription ID.

**Save the output of this command.** You will need the following values to configure Jenkins credentials:

-   `appId` (This is your **CLIENT_ID**)
-   `password` (This is your **CLIENT_SECRET**)
-   `tenant` (This is your **TENANT_ID**)

## 3. Run Terraform Manually (First Test)

It's recommended to run Terraform manually once to ensure your configuration is correct and to provision the initial resources. Navigate to the `terraform` directory:

```bash
cd terraform
terraform init
terraform plan
terraform apply -auto-approve
```

This will initialize Terraform, show you the planned changes, and then apply them to create the Azure Resource Group, Storage Account, and Storage Container.

## 4. Get Storage Account Connection String

After the storage account is created, retrieve its connection string. This will be used by the backup system to connect to the Azure Blob Storage (in a real scenario, our simulator uses a local path).

```bash
az storage account show-connection-string \
  --name backupstorage123 \
  --resource-group backup-rg
```

**Note:** In our simulated environment, the `cloud_simulator.py` uses `local_storage_path` from `config.py`. For a real Azure deployment, you would configure your application to use this connection string.

## 5. Push Code - Jenkins Will Auto-Deploy

Once your Jenkins pipeline is configured (as per `JENKINS_SETUP.md`) and connected to your GitHub repository, any push to the `main` branch will trigger the CI/CD pipeline, which includes the deployment steps.

```bash
git push origin main
```

## 6. Watch the Pipeline

Monitor the progress of your deployment in Jenkins:

-   Access Jenkins at `http://localhost:8080`.
-   Go to your `disaster-recovery-pipeline` job.
-   Click on the latest build to view the console output and stage progress.

The pipeline will execute the stages defined in `jenkins/Jenkinsfile`, including building the Docker image, provisioning infrastructure with Terraform, and deploying the application.

```