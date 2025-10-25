"""Configuration Management for Backup System"""
import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data" / "sample_data"
BACKUP_DIR = BASE_DIR / "backups"
LOG_DIR = BASE_DIR / "logs"

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
BACKUP_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Backup configuration
BACKUP_CONFIG = {
    "source_dirs": [str(DATA_DIR)],
    "backup_location": str(BACKUP_DIR),
    "retention_days": 30,
    "compression": "zip",
    "include_db": False,
}

# Cloud simulation configuration
CLOUD_CONFIG = {
    "provider": "azure_blob_simulator",
    "container_name": "backups",
    "storage_account": "backupstorage123",
    "simulate_locally": True,
    "local_storage_path": str(BACKUP_DIR),
}

# Logging configuration
LOG_CONFIG = {
    "log_file": str(LOG_DIR / "backup_system.log"),
    "log_level": "INFO",
    "max_log_size_mb": 10,
}

# Jenkins simulation
JENKINS_CONFIG = {
    "pipeline_stages": [
        "Provision Infrastructure",
        "Run Backup",
        "Upload to Cloud",
        "Verify Backup",
        "Send Notification"
    ]
}

# Terraform simulation
TERRAFORM_CONFIG = {
    "resource_group": "backup-rg",
    "location": "East US",
    "storage_account": "backupstorage123",
    "container_name": "backups",
}