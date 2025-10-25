"""Enhanced Tkinter GUI Dashboard for Backup System"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
import os
from pathlib import Path
import threading
import time
import datetime
import psutil # For system monitoring

sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from backup import BackupSystem
from restore import RestoreSystem
from cloud_simulator import CloudStorageSimulator
from config import TERRAFORM_CONFIG, JENKINS_CONFIG, LOG_CONFIG

# Configure logging for the GUI
import logging
logging.basicConfig(
    filename=LOG_CONFIG["log_file"],
    level=LOG_CONFIG["log_level"],
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class BackupDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ Automated Disaster Recovery Dashboard (Enhanced)")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2C3E50')
        
        self.backup_system = BackupSystem()
        self.restore_system = RestoreSystem()
        self.cloud_simulator = CloudStorageSimulator()
        
        # Session statistics
        self.backups_created_session = 0
        self.disasters_handled_session = 0
        self.restores_completed_session = 0
        self.system_health = 100 # Percentage
        self.disaster_state = "Normal" # "Normal", "Server Crash", "Server Overload", "Total Loss", "Data Corruption"
        self.auto_backup_enabled = False
        self.auto_backup_thread = None

        self.setup_ui()
        self.refresh_dashboard()
        self.start_system_monitor()
    
    def setup_ui(self):
        """Setup the main UI"""
        
        # Title
        title_frame = tk.Frame(self.root, bg='#34495E', pady=15)
        title_frame.pack(fill=tk.X)
        
        tk.Label(title_frame, text="🛡️ Automated Disaster Recovery Backup System (Enhanced)",
                font=('Arial', 18, 'bold'), bg='#34495E', fg='white').pack()
        tk.Label(title_frame, text="DevOps Automation | CI/CD | Infrastructure as Code | Monitoring",
                font=('Arial', 10), bg='#34495E', fg='#BDC3C7').pack()
        
        # Main content
        main_frame = tk.Frame(self.root, bg='#2C3E50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Actions
        left_panel = tk.Frame(main_frame, bg='#34495E', width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))
        
        # Right panel - Info and Monitoring
        right_panel = tk.Frame(main_frame, bg='#34495E')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.setup_left_panel(left_panel)
        self.setup_right_panel(right_panel)
    
    def setup_left_panel(self, parent):
        """Setup action buttons"""
        
        self.create_section(parent, "🏗️ Infrastructure (Terraform)")
        self.create_button(parent, "Provision Infrastructure", self.provision_infrastructure, '#3498DB')
        
        self.create_section(parent, "💾 Backup Operations")
        self.create_button(parent, "Run Backup Now", self.run_backup, '#27AE60')
        self.create_button(parent, "View Backups", self.view_backups, '#16A085')
        self.create_button(parent, "Restore Backup", self.restore_backup_action, '#F39C12')
        
        self.create_section(parent, "🚨 Disaster Simulation")
        self.create_button(parent, "Simulate Server Crash", lambda: self.simulate_disaster("Server Crash"), '#E74C3C')
        self.create_button(parent, "Simulate Server Overload", lambda: self.simulate_disaster("Server Overload"), '#E67E22')
        self.create_button(parent, "Destroy Server (Total Loss)", lambda: self.simulate_disaster("Total Loss"), '#C0392B')
        self.create_button(parent, "Data Corruption", lambda: self.simulate_disaster("Data Corruption"), '#8E44AD')
        self.create_button(parent, "Emergency Recovery", self.emergency_recovery, '#2ECC71')

        self.create_section(parent, "⚙️ Automation")
        self.auto_backup_button = self.create_button(parent, "Enable Auto-Backup", self.toggle_auto_backup, '#34495E')
        self.auto_backup_status_label = tk.Label(parent, text="⚪ DISABLED", bg='#34495E', fg='white', font=('Arial', 10, 'bold'))
        self.auto_backup_status_label.pack(fill=tk.X, padx=10, pady=2)

        self.create_section(parent, "🔄 CI/CD Operations")
        self.create_button(parent, "Trigger Jenkins Build", self.run_jenkins_pipeline, '#9B59B6')
        self.create_button(parent, "Deploy to Azure", lambda: self.log("Simulating Azure Deployment..."), '#3498DB')
        self.create_button(parent, "Provision Azure Resources", self.provision_infrastructure, '#3498DB') # Re-use existing

        self.create_section(parent, "📊 Monitoring & Utilities")
        self.create_button(parent, "View Logs", self.view_logs, '#34495E')
        self.create_button(parent, "Refresh Dashboard", self.refresh_dashboard, '#7F8C8D')
        self.create_button(parent, "Show Docker Info", self.show_docker_info, '#2980B9')
    
    def setup_right_panel(self, parent):
        """Setup information display and monitoring"""
        
        # System Monitoring
        monitor_frame = tk.LabelFrame(parent, text="💻 System Monitoring", font=('Arial', 12, 'bold'),
                                      bg='#34495E', fg='white', padx=10, pady=10)
        monitor_frame.pack(fill=tk.X, padx=10, pady=5)

        self.cpu_label = self.create_monitor_label(monitor_frame, "CPU Usage:")
        self.cpu_progress = ttk.Progressbar(monitor_frame, orient="horizontal", length=200, mode="determinate")
        self.cpu_progress.pack(fill=tk.X, padx=5, pady=2)

        self.mem_label = self.create_monitor_label(monitor_frame, "Memory Usage:")
        self.mem_progress = ttk.Progressbar(monitor_frame, orient="horizontal", length=200, mode="determinate")
        self.mem_progress.pack(fill=tk.X, padx=5, pady=2)

        self.disk_label = self.create_monitor_label(monitor_frame, "Disk Usage:")
        self.disk_progress = ttk.Progressbar(monitor_frame, orient="horizontal", length=200, mode="determinate")
        self.disk_progress.pack(fill=tk.X, padx=5, pady=2)

        self.uptime_label = self.create_monitor_label(monitor_frame, "Uptime:")
        self.disaster_state_label = self.create_monitor_label(monitor_frame, "Disaster State:")
        self.system_health_label = self.create_monitor_label(monitor_frame, "System Health:")

        # Enhanced Statistics
        tk.Label(parent, text="📊 System Statistics", font=('Arial', 14, 'bold'),
                bg='#34495E', fg='white', pady=10).pack(fill=tk.X)
        
        self.stats_text = scrolledtext.ScrolledText(parent, height=12, bg='#ECF0F1',
                                                     fg='#2C3E50', font=('Courier', 10), wrap=tk.WORD)
        self.stats_text.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(parent, text="📝 Console Output", font=('Arial', 14, 'bold'),
                bg='#34495E', fg='white', pady=10).pack(fill=tk.X)
        
        self.console_text = scrolledtext.ScrolledText(parent, bg='#1C1C1C', fg='#00FF00',
                                                       font=('Courier', 9), wrap=tk.WORD)
        self.console_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.status_bar = tk.Label(parent, text="Ready", bg='#27AE60', fg='white',
                                   anchor=tk.W, padx=10, pady=5, font=('Arial', 9))
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def create_monitor_label(self, parent, text):
        label = tk.Label(parent, text=text, bg='#34495E', fg='#BDC3C7', font=('Arial', 10))
        label.pack(fill=tk.X, padx=5, pady=2, anchor=tk.W)
        return label
    
    def create_section(self, parent, title):
        """Create section header"""
        tk.Label(parent, text=title, font=('Arial', 11, 'bold'),
                bg='#34495E', fg='white', pady=8).pack(fill=tk.X, padx=10, pady=(10, 0))
    
    def create_button(self, parent, text, command, color):
        """Create styled button"""
        button = tk.Button(parent, text=text, command=command, bg=color, fg='white',
                          font=('Arial', 10, 'bold'), cursor='hand2', relief=tk.FLAT,
                          padx=15, pady=10)
        button.pack(fill=tk.X, padx=10, pady=5)
        return button
    
    def log(self, message, level="info"):
        """Log message to console and file"""
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        display_message = f"[{timestamp}] {message}\n"
        self.console_text.insert(tk.END, display_message)
        self.console_text.see(tk.END)
        
        if level == "info":
            logging.info(message)
        elif level == "warning":
            logging.warning(message)
        elif level == "error":
            logging.error(message)
        
        self.root.update_idletasks() # Update GUI immediately
    
    def update_status(self, message, bg='#27AE60'):
        """Update status bar"""
        self.status_bar.config(text=message, bg=bg)
        self.root.update_idletasks() # Update GUI immediately
    
    def start_system_monitor(self):
        """Start a thread to monitor system resources"""
        def monitor():
            while True:
                self.update_system_stats()
                time.sleep(1) # Update every second
        
        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()

    def update_system_stats(self):
        """Fetch and update system resource statistics"""
        cpu_percent = psutil.cpu_percent(interval=None)
        mem_info = psutil.virtual_memory()
        disk_info = psutil.disk_usage('/')
        
        boot_time_timestamp = psutil.boot_time()
        boot_time_datetime = datetime.datetime.fromtimestamp(boot_time_timestamp)
        uptime = datetime.datetime.now() - boot_time_datetime

        self.cpu_label.config(text=f"CPU Usage: {cpu_percent:.1f}%")
        self.cpu_progress["value"] = cpu_percent

        self.mem_label.config(text=f"Memory Usage: {mem_info.percent:.1f}%")
        self.mem_progress["value"] = mem_info.percent

        self.disk_label.config(text=f"Disk Usage: {disk_info.percent:.1f}%")
        self.disk_progress["value"] = disk_info.percent

        self.uptime_label.config(text=f"Uptime: {str(uptime).split('.')[0]}") # Remove microseconds
        self.disaster_state_label.config(text=f"Disaster State: {self.disaster_state}")
        self.system_health_label.config(text=f"System Health: {self.system_health:.1f}%")

        # Update status bar color based on health
        if self.system_health < 30:
            self.status_bar.config(bg='#C0392B') # Red
        elif self.system_health < 70:
            self.status_bar.config(bg='#E67E22') # Orange
        else:
            self.status_bar.config(bg='#27AE60') # Green

    def provision_infrastructure(self):
        """Simulate Terraform provisioning"""
        self.update_status("Provisioning infrastructure...", '#3498DB')
        self.log("=" * 60)
        self.log("🏗️ TERRAFORM INFRASTRUCTURE PROVISIONING")
        self.log("=" * 60)
        
        def provision():
            steps = [
                ("Initializing Terraform", 1),
                ("Planning infrastructure", 1.5),
                (f"Creating Resource Group: {TERRAFORM_CONFIG['resource_group']}", 1),
                (f"Creating Storage Account: {TERRAFORM_CONFIG['storage_account']}", 1.5),
                (f"Creating Container: {TERRAFORM_CONFIG['container_name']}", 1),
                ("Applying security policies", 1),
                ("Infrastructure ready", 0.5)
            ]
            
            for step, delay in steps:
                self.log(f"  → {step}...")
                time.sleep(delay)
            
            self.log("✅ Infrastructure provisioned successfully!")
            self.update_status("Infrastructure ready", '#27AE60')
            messagebox.showinfo("Success", f"Infrastructure provisioned!\n\nResource Group: {TERRAFORM_CONFIG['resource_group']}\nLocation: {TERRAFORM_CONFIG['location']}")
        
        threading.Thread(target=provision, daemon=True).start()
    
    def run_backup(self):
        """Run backup"""
        self.update_status("Running backup...", '#F39C12')
        self.log("=" * 60)
        self.log("💾 STARTING BACKUP OPERATION")
        self.log("=" * 60)
        
        def backup():
            success, backup_name, metadata = self.backup_system.create_backup()
            
            if success:
                self.log(f"✅ Backup: {backup_name}")
                self.log(f"   Files: {metadata['total_files']}")
                self.log(f"   Size: {metadata['total_size_mb']} MB")
                self.log("☁️  Uploaded to cloud")
                self.backups_created_session += 1
                self.update_status("Backup completed", '#27AE60')
                self.refresh_dashboard()
                messagebox.showinfo("Success", f"Backup completed!\n\nFiles: {metadata['total_files']}\nSize: {metadata['total_size_mb']} MB")
            else:
                self.log("❌ Backup failed!", level="error")
                self.update_status("Backup failed", '#E74C3C')
        
        threading.Thread(target=backup, daemon=True).start()
    
    def view_backups(self):
        """Show backups"""
        backups = self.backup_system.list_backups()
        
        if not backups:
            messagebox.showinfo("No Backups", "No backups found.")
            return
        
        popup = tk.Toplevel(self.root)
        popup.title("Available Backups")
        popup.geometry("700x400")
        popup.configure(bg='#34495E')
        
        tk.Label(popup, text="📦 Available Backups", font=('Arial', 14, 'bold'),
                bg='#34495E', fg='white', pady=10).pack()
        
        frame = tk.Frame(popup, bg='#34495E')
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set,
                            bg='#ECF0F1', font=('Courier', 10), selectmode=tk.SINGLE)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        for backup in backups:
            text = f"{backup['backup_name']}  |  {backup.get('total_files', 'N/A')} files  |  {backup.get('total_size_mb', 'N/A')} MB"
            listbox.insert(tk.END, text)
        
        btn_frame = tk.Frame(popup, bg='#34495E', pady=10)
        btn_frame.pack(fill=tk.X)
        
        def restore_selected():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Select a backup first.")
                return
            backup_name = backups[selection[0]]['backup_name']
            popup.destroy()
            self.restore_specific_backup(backup_name)
        
        tk.Button(btn_frame, text="Restore", command=restore_selected,
                 bg='#27AE60', fg='white', font=('Arial', 10, 'bold'), padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Close", command=popup.destroy,
                 bg='#7F8C8D', fg='white', font=('Arial', 10, 'bold'), padx=20, pady=5).pack(side=tk.RIGHT, padx=5)
    
    def restore_backup_action(self):
        """Action to trigger restore from UI"""
        self.view_backups()
    
    def restore_specific_backup(self, backup_name):
        """Restore specific backup"""
        self.update_status("Restoring...", '#F39C12')
        self.log("=" * 60)
        self.log(f"♻️  RESTORING: {backup_name}")
        self.log("=" * 60)
        
        def restore():
            success = self.restore_system.restore_backup(backup_name)
            if success:
                self.log("✅ Restore complete!")
                self.restores_completed_session += 1
                self.system_health = 100 # Restore health after recovery
                self.disaster_state = "Normal"
                self.update_status("Restored", '#27AE60')
                messagebox.showinfo("Success", f"Backup restored!\n\n{backup_name}")
            else:
                self.log("❌ Restore failed!", level="error")
                self.update_status("Failed", '#E74C3C')
        
        threading.Thread(target=restore, daemon=True).start()

    def simulate_disaster(self, disaster_type):
        """Simulate various disaster scenarios"""
        self.disasters_handled_session += 1
        self.disaster_state = disaster_type
        self.log(f"🚨 SIMULATING DISASTER: {disaster_type}!", level="error")
        self.update_status(f"🔴 DISASTER: {disaster_type}!", '#E74C3C')

        if disaster_type == "Server Crash":
            self.system_health = 0
            self.log("System health dropped to 0%. Triggering emergency backup...")
            self.run_backup() # Trigger emergency backup
        elif disaster_type == "Server Overload":
            self.system_health = 20
            self.log("CPU 98%, Memory 95%. Triggering emergency backup...")
            # Simulate high CPU/Mem usage for a short period
            self.cpu_progress["value"] = 98
            self.mem_progress["value"] = 95
            self.run_backup()
        elif disaster_type == "Total Loss":
            self.system_health = 0
            self.log("Complete system failure. Data might be lost. Triggering emergency backup (if possible)...")
            self.run_backup()
        elif disaster_type == "Data Corruption":
            self.system_health = 50
            self.log("Database corruption detected. Triggering emergency backup...")
            self.run_backup()
        
        self.refresh_dashboard()

    def emergency_recovery(self):
        """Initiate emergency recovery using the latest backup"""
        self.log("🚨 Initiating Emergency Recovery...")
        self.update_status("Emergency Recovery in progress...", '#F39C12')
        
        def recover():
            backups = self.backup_system.list_backups()
            if not backups:
                self.log("No backups available for emergency recovery.", level="error")
                messagebox.showerror("Error", "No backups available for emergency recovery.")
                self.update_status("Recovery failed", '#E74C3C')
                return
            
            latest_backup = backups[0]['backup_name']
            self.log(f"Automatically selecting latest backup: {latest_backup}")
            self.restore_specific_backup(latest_backup)
            self.log("✅ Emergency Recovery complete!")
            self.update_status("Recovery complete", '#2ECC71')
        
        threading.Thread(target=recover, daemon=True).start()

    def toggle_auto_backup(self):
        """Toggle automated backup feature"""
        self.auto_backup_enabled = not self.auto_backup_enabled
        if self.auto_backup_enabled:
            self.auto_backup_button.config(text="Disable Auto-Backup", bg='#E74C3C')
            self.auto_backup_status_label.config(text="🟢 ENABLED", fg='#2ECC71')
            self.log("Auto-Backup ENABLED. Running every 5 minutes.")
            self.auto_backup_thread = threading.Thread(target=self._auto_backup_loop, daemon=True)
            self.auto_backup_thread.start()
        else:
            self.auto_backup_button.config(text="Enable Auto-Backup", bg='#34495E')
            self.auto_backup_status_label.config(text="⚪ DISABLED", fg='white')
            self.log("Auto-Backup DISABLED.")
            # The daemon thread will naturally exit when the main program exits,
            # or we could add a flag to its loop to stop it more gracefully.
            # For simplicity, we'll let it run until the app closes or just stop scheduling new backups.

    def _auto_backup_loop(self):
        """Loop for automated backups"""
        while self.auto_backup_enabled:
            self.log("Auto-Backup: Triggering automated backup...")
            self.run_backup()
            for _ in range(300): # Wait for 5 minutes (300 seconds)
                if not self.auto_backup_enabled:
                    break # Exit if disabled during wait
                time.sleep(1)
            
    def run_jenkins_pipeline(self):
        """Simulate Jenkins pipeline trigger"""
        self.update_status("Triggering Jenkins pipeline...", '#9B59B6')
        self.log("=" * 60)
        self.log("🔄 JENKINS CI/CD PIPELINE TRIGGERED")
        self.log("=" * 60)
        
        def pipeline_simulation():
            self.log("Simulating Jenkins pipeline stages...")
            for i, stage in enumerate(JENKINS_CONFIG['pipeline_stages'], 1):
                self.log(f"Stage {i}: {stage}")
                time.sleep(1.5) # Simulate work
                if stage == "Run Backup":
                    success, backup_name, metadata = self.backup_system.create_backup()
                    if success:
                        self.log(f"  ✅ Created: {backup_name}")
                else:
                    self.log(f"  ✅ Complete")
            
            self.log("🎉 Jenkins Pipeline complete!")
            self.update_status("Pipeline complete", '#27AE60')
            self.refresh_dashboard()
            messagebox.showinfo("Jenkins", "Pipeline completed!")
        
        threading.Thread(target=pipeline_simulation, daemon=True).start()
    
    def view_logs(self):
        """View logs"""
        log_file = Path(__file__).parent.parent / "logs" / "backup_system.log"
        
        if not log_file.exists():
            messagebox.showinfo("No Logs", "No log file found.")
            return
        
        popup = tk.Toplevel(self.root)
        popup.title("System Logs")
        popup.geometry("800x500")
        popup.configure(bg='#2C3E50')
        
        tk.Label(popup, text="📝 System Logs", font=('Arial', 14, 'bold'),
                bg='#2C3E50', fg='white', pady=10).pack()
        
        log_text = scrolledtext.ScrolledText(popup, bg='#1C1C1C', fg='#00FF00',
                                             font=('Courier', 9), wrap=tk.WORD)
        log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        with open(log_file, 'r') as f:
            log_text.insert(tk.END, f.read())
            log_text.see(tk.END)
        
        tk.Button(popup, text="Close", command=popup.destroy,
                 bg='#7F8C8D', fg='white', font=('Arial', 10, 'bold'),
                 padx=20, pady=5).pack(pady=10)
    
    def show_docker_info(self):
        """Show Docker info"""
        info = """DOCKER DEPLOYMENT

Build: docker build -t backup-system -f docker/Dockerfile .
Run: docker run -v $(pwd)/data:/app/data backup-system
Compose: docker-compose -f docker/docker-compose.yml up

Includes: Python 3.9, all dependencies, automation
"""
        self.log("=" * 60)
        self.log(info)
        messagebox.showinfo("Docker", info)
    
    def refresh_dashboard(self):
        """Refresh stats"""
        try:
            backup_stats = self.backup_system.get_backup_stats()
            cloud_stats = self.cloud_simulator.get_storage_stats()
            
            stats = f"""
╔══════════════════════════════════════════╗
║  BACKUP STATISTICS                       ║
╠══════════════════════════════════════════╣
║  Total Backups (All Time): {backup_stats['total_backups']:<15} ║
║  Total Size (All Time):    {backup_stats['total_size_mb']} MB{' ' * (15 - len(str(backup_stats['total_size_mb'])))} ║
║  Latest Backup:            {backup_stats['latest_backup'][:20]:<15}║
╠══════════════════════════════════════════╣
║  SESSION STATISTICS                      ║
╠══════════════════════════════════════════╣
║  Backups Created:          {self.backups_created_session:<15} ║
║  Disasters Handled:        {self.disasters_handled_session:<15} ║
║  Restores Completed:       {self.restores_completed_session:<15} ║
╠══════════════════════════════════════════╣
║  CLOUD STORAGE (Simulated)               ║
╠══════════════════════════════════════════╣
║  Total Blobs:              {cloud_stats['total_blobs']:<15} ║
║  Total Size:               {cloud_stats['total_size_mb']} MB{' ' * (15 - len(str(cloud_stats['total_size_mb'])))} ║
╚══════════════════════════════════════════╝
            """
            
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(tk.END, stats.strip())
            # Status bar is updated by system monitor or specific actions
        except Exception as e:
            self.log(f"Error refreshing dashboard: {str(e)}", level="error")

def main():
    root = tk.Tk()
    app = BackupDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()
