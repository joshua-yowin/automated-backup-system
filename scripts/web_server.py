from flask import Flask, jsonify
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from backup import BackupSystem

app = Flask(__name__)
backup_system = BackupSystem()

@app.route("/health")
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "Backup system web server is running."
    })

@app.route("/metrics")
def metrics():
    # In a real scenario, you would expose actual metrics here
    # For now, we'll return some dummy data or basic stats
    backup_stats = backup_system.get_backup_stats()
    return jsonify({
        "total_backups": backup_stats["total_backups"],
        "total_size_mb": backup_stats["total_size_mb"],
        "latest_backup": backup_stats["latest_backup"],
        "system_health": 100 # Placeholder
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
