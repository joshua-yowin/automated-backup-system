# Automated Backup System

This project is an enhanced simulation of an automated disaster recovery backup system, incorporating advanced monitoring, CI/CD, and infrastructure as code principles.

## Features

-   **Automated Backups:** Create backups of specified directories.
-   **Cloud Simulation:** Simulates uploading backups to Azure Blob Storage.
-   **Restore Functionality:** Restore backups to a specified location.
-   **Enhanced GUI Dashboard:** A Tkinter-based dashboard with real-time monitoring, disaster simulation, and CI/CD operations.
-   **CI/CD Pipeline:** A Jenkinsfile to simulate a comprehensive CI/CD pipeline with 10 stages.
-   **Infrastructure as Code:** Terraform configuration to provision simulated Azure resources.
-   **Docker Support:** Dockerfile and docker-compose.yml for containerization and orchestration.
-   **System Monitoring:** Real-time CPU, Memory, Disk usage, and Uptime display.
-   **Disaster Simulation:** Buttons to simulate various disaster scenarios (Server Crash, Overload, Total Loss, Data Corruption).
-   **Auto-Backup Feature:** Toggle for automated backups every 5 minutes.
-   **Web Interface:** A simple Flask web server for health checks and metrics.

## Project Structure

```
automated-backup-system/
├── app/
│   ├── __init__.py
│   ├── config.py                    # Configuration management
│   ├── backup.py                    # Core backup logic
│   ├── restore.py                   # Restore functionality
│   └── cloud_simulator.py           # Azure simulator
│
├── dashboard/
│   ├── __init__.py
│   └── gui_enhanced.py              # Enhanced Tkinter GUI
│
├── jenkins/
│   └── Jenkinsfile                  # CI/CD pipeline
│
├── terraform/
│   ├── main.tf                      # Azure infrastructure
│   ├── variables.tf                 # Configuration variables
│   └── outputs.tf                   # Resource outputs
│
├── docker/
│   ├── Dockerfile                   # Multi-stage production build
│   └── prometheus.yml               # Monitoring config
│
├── scripts/
│   ├── scheduler.py                 # Automated backup scheduler
│   └── web_server.py                # Flask web interface
│
├── docs/
│   ├── JENKINS_SETUP.md            # Complete Jenkins guide
│   ├── AZURE_DEPLOYMENT.md         # Azure deployment steps
│   └── DOCKER_GUIDE.md             # Docker best practices
│
├── data/sample_data/                # Sample files for backup
├── backups/                         # Backup storage
├── logs/                            # System logs
├── docker-compose.yml               # Complete stack orchestration
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment template
└── README.md                        # Project documentation
```

## Getting Started

### Phase 1: Local Testing (without Docker)

1.  **Navigate to Project Directory:**

    ```bash
    cd automated-backup-system
    ```

2.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Enhanced Dashboard:**

    ```bash
    python dashboard/gui_enhanced.py
    ```

4.  **Test Disaster Simulation:**
    -   Click "Simulate Server Crash"
    -   Observe automatic backup trigger
    -   Click "Emergency Recovery"
    -   Verify system restored

### Phase 2: Docker Local Testing

1.  **Build Image:**

    ```bash
    docker build -t backup-system:dev -f docker/Dockerfile .
    ```

2.  **Run Locally (Single Container):**

    ```bash
docker run -it --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/backups:/app/backups \
  backup-system:dev
    ```

3.  **Test Backup Inside Container:**

    ```bash
docker exec -it <container-id> python3 app/backup.py
    ```

4.  **Verify Files:**

    ```bash
    ls -lh backups/
    ```

### Phase 3: Jenkins Setup

Refer to `docs/JENKINS_SETUP.md` for detailed instructions on setting up Jenkins, installing plugins, and configuring credentials.

### Phase 4: GitHub Integration

Refer to `docs/DOCKER_GUIDE.md` for instructions on building and running Docker images, and `docs/AZURE_DEPLOYMENT.md` for Azure deployment steps.

### Phase 5: Azure Deployment

Refer to `docs/AZURE_DEPLOYMENT.md` for detailed instructions on Azure login, creating a service principal, running Terraform, and getting storage connection strings.

## Testing the Complete System

### Test Scenario 1: Disaster Detection & Recovery

1.  **Start Enhanced Dashboard:**

    ```bash
    python dashboard/gui_enhanced.py
    ```

2.  **Simulate Disaster:**
    -   Click: "Simulate Server Crash"
    -   **Observe:**
        -   System health drops to 0%
        -   Status bar turns red: "🔴 DISASTER: Server crashed!"
        -   Automatic backup triggers
        -   Console shows: "🚨 Triggering emergency backup..."

3.  **Run Emergency Recovery:**
    -   Click: "Emergency Recovery"
    -   **Observe:**
        -   Latest backup automatically selected
        -   Files extracted to `restored_<timestamp>/`
        -   System health restored to 100%
        -   Status: "✅ Recovery complete"

    *Time: < 30 seconds for complete disaster recovery!* 

### Test Scenario 2: CI/CD Pipeline

1.  **Make Code Change:**

    ```bash
    echo "# Update" >> README.md
    ```

2.  **Commit and Push:**

    ```bash
    git add README.md
    git commit -m "Trigger CI/CD"
    git push origin main
    ```

3.  **Watch Jenkins:** (`http://localhost:8080`)
    -   Pipeline automatically executes all 10 stages.

    *Total time: ~6-7 minutes*
    *Result: Application deployed to Azure!* 

### Test Scenario 3: Docker Stack

1.  **Start Complete Stack:**

    ```bash
    docker-compose up -d
    ```

2.  **Verify All Services:**

    ```bash
    docker-compose ps
    ```

3.  **Test Backup Service:**

    ```bash
    docker-compose exec backup-service python3 app/backup.py
    ```

4.  **View Scheduler Logs:**

    ```bash
    docker-compose logs -f backup-scheduler
    ```

5.  **Access Web Dashboard:**

    ```bash
    curl http://localhost:5000/health
    ```

6.  **Scale Backup Services:**

    ```bash
    docker-compose up --scale backup-service=3 -d
    ```# Update
