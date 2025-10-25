"""Cloud Storage Simulator - Simulates Azure Blob Storage locally"""
import json
from pathlib import Path
from datetime import datetime
from config import CLOUD_CONFIG, LOG_CONFIG
import logging

logging.basicConfig(
    filename=LOG_CONFIG["log_file"],
    level=LOG_CONFIG["log_level"],
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class CloudStorageSimulator:
    """Simulates cloud storage operations locally"""
    
    def __init__(self):
        self.config = CLOUD_CONFIG
        self.storage_path = Path(self.config["local_storage_path"])
        self.container_name = self.config["container_name"]
        self.metadata_file = self.storage_path / "cloud_metadata.json"
        self._load_metadata()
    
    def _load_metadata(self):
        """Load cloud storage metadata"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {
                "container_name": self.container_name,
                "storage_account": self.config["storage_account"],
                "blobs": [],
                "created_at": datetime.now().isoformat()
            }
            self._save_metadata()
    
    def _save_metadata(self):
        """Save cloud storage metadata"""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def upload_backup(self, backup_path, backup_metadata):
        """Simulate uploading backup to cloud storage"""
        try:
            backup_path = Path(backup_path)
            logging.info(f"Simulating cloud upload: {backup_path.name}")
            
            blob_info = {
                "blob_name": backup_path.name,
                "size_bytes": backup_path.stat().st_size,
                "size_mb": round(backup_path.stat().st_size / (1024 * 1024), 2),
                "uploaded_at": datetime.now().isoformat(),
                "metadata": backup_metadata
            }
            
            self.metadata["blobs"].append(blob_info)
            self._save_metadata()
            logging.info(f"Cloud upload simulated successfully: {backup_path.name}")
            return True
        except Exception as e:
            logging.error(f"Cloud upload simulation failed: {str(e)}")
            return False
    
    def list_blobs(self):
        """List all blobs in cloud storage"""
        return self.metadata.get("blobs", [])
    
    def get_storage_stats(self):
        """Get storage statistics"""
        total_size = sum(blob.get("size_mb", 0) for blob in self.metadata.get("blobs", []))
        return {
            "total_blobs": len(self.metadata.get("blobs", [])),
            "total_size_mb": round(total_size, 2),
            "container_name": self.container_name,
            "storage_account": self.config["storage_account"]
        }