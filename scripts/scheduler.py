import time
import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from backup import BackupSystem
from config import LOG_CONFIG
import logging

logging.basicConfig(
    filename=LOG_CONFIG["log_file"],
    level=LOG_CONFIG["log_level"],
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_scheduler():
    backup_system = BackupSystem()
    logging.info("Backup scheduler started - runs every 5 minutes")
    print("🕐 Backup scheduler started - runs every 5 minutes")
    while True:
        logging.info(f"Scheduler: Running automated backup at {datetime.datetime.now()}")
        print(f"Scheduler: Running automated backup at {datetime.datetime.now()}")
        success, backup_name, metadata = backup_system.create_backup()
        if success:
            logging.info(f"Scheduler: Automated backup {backup_name} completed successfully.")
            print(f"Scheduler: Automated backup {backup_name} completed successfully.")
        else:
            logging.error(f"Scheduler: Automated backup failed.")
            print(f"Scheduler: Automated backup failed.")
        time.sleep(300) # Run every 5 minutes (300 seconds)

if __name__ == "__main__":
    run_scheduler()
