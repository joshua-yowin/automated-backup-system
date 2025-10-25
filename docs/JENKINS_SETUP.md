# Jenkins Setup Guide

This guide outlines the steps to set up Jenkins for the Automated Backup System CI/CD pipeline.

## 1. Start Jenkins with Docker Compose

Navigate to the root of your project and start the Jenkins service using Docker Compose:

```bash
docker-compose up -d jenkins
```

## 2. Get Initial Admin Password

Once Jenkins is running, retrieve the initial administrator password from the Jenkins container logs:

```bash
docker-compose exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

## 3. Access Jenkins

Open your web browser and navigate to the Jenkins interface:

[http://localhost:8080](http://localhost:8080)

Use `admin` as the username and the password obtained in the previous step to log in.

## 4. Install Required Plugins

After logging in, proceed to install the necessary plugins. Go to `Dashboard` → `Manage Jenkins` → `Manage Plugins` → `Available plugins` and install the following:

-   **GitHub Integration**
-   **Docker Pipeline**
-   **Azure Credentials**
-   **Terraform**

## 5. Add Credentials

Configure the required credentials in Jenkins. Go to `Dashboard` → `Manage Jenkins` → `Manage Credentials` → `System` → `Global credentials (unrestricted)` → `Add Credentials`.

Add the following credentials:

-   **GitHub token:** A personal access token with `repo` scope.
-   **Azure service principal:** Use the `Microsoft Azure Service Principal` kind. You will need:
    -   `Subscription ID`
    -   `Tenant ID`
    -   `Client ID` (appId)
    -   `Client Secret` (password)
-   **Docker Hub credentials:** For pushing Docker images to Docker Hub.
-   **Azure storage connection string:** For interacting with Azure Storage.

## 6. Create Pipeline Job

Create a new Jenkins pipeline job:

1.  Go to `Dashboard` → `New Item`.
2.  Enter an item name, e.g., `disaster-recovery-pipeline`.
3.  Select `Pipeline` and click `OK`.
4.  In the job configuration:
    -   Under `General`, check `GitHub project` and provide your GitHub repository URL.
    -   Under `Build Triggers`, check `GitHub hook trigger for GITScm polling`.
    -   Under `Pipeline`, select `Pipeline script from SCM`.
    -   **SCM:** `Git`
    -   **Repository URL:** `https://github.com/your-username/backup-system.git` (Replace with your actual repository URL)
    -   **Credentials:** Select your GitHub credentials.
    -   **Branches to build:** `*/main`
    -   **Script Path:** `jenkins/Jenkinsfile`

Click `Save` to create the pipeline job.
