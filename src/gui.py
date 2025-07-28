"""
Tkinter GUI for Ruddibaba Optimizer
"""
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from datetime import datetime

# Handle imports for both direct execution and package import
try:
    # When running as part of the package
    from ..core import SafeOptimizer, OptionalOptimizer, HardcoreOptimizer, OptimizationLevel
    from ..core.logger import setup_logging
    from ..core.backup import BackupManager
except ImportError:
    # When running this file directly
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from src.core import SafeOptimizer, OptionalOptimizer, HardcoreOptimizer, OptimizationLevel
    from src.core.logger import setup_logging
    from src.core.backup import BackupManager

class RuddibabaOptimizerGUI:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.setup_styles()
        self.logger = setup_logging().get_logger(__name__)
        self.backup_manager = BackupManager()
        
    def setup_ui(self):
        """Set up the main UI components"""
        self.root.title("Ruddibaba Optimizer")
        self.root.geometry("800x600")
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        ttk.Label(
            main_frame, 
            text="Ruddibaba Optimizer", 
            font=('Segoe UI', 16, 'bold')
        ).pack(pady=(0, 10))
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_optimize_tab()
        self.create_logs_tab()
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(
            main_frame, 
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            padding=5
        ).pack(fill=tk.X, pady=(10, 0))
    
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', padding=5)
        style.configure('TNotebook.Tab', padding=[10, 5])
    
    def create_optimize_tab(self):
        """Create the optimization tab"""
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="Optimize")
        
        # Optimization level
        level_frame = ttk.LabelFrame(tab, text="Optimization Level", padding=10)
        level_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.optimization_level = tk.StringVar(value="safe")
        
        levels = [
            ("Safe", "safe", "Basic optimizations that are safe for all systems"),
            ("Optional", "optional", "Performance-focused tweaks"),
            ("Hardcore", "hardcore", "Advanced optimizations (use with caution!)")
        ]
        
        for text, value, desc in levels:
            ttk.Radiobutton(
                level_frame,
                text=f"{text}: {desc}",
                variable=self.optimization_level,
                value=value
            ).pack(anchor=tk.W, pady=2)
        
        # Options
        options_frame = ttk.LabelFrame(tab, text="Options", padding=10)
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.create_backup = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            options_frame,
            text="Create backup before making changes",
            variable=self.create_backup
        ).pack(anchor=tk.W)
        
        # Action buttons
        button_frame = ttk.Frame(tab)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.optimize_btn = ttk.Button(
            button_frame,
            text="Run Optimizations",
            command=self.run_optimizations
        )
        self.optimize_btn.pack(side=tk.RIGHT, padx=5)
        
        self.cancel_btn = ttk.Button(
            button_frame,
            text="Cancel",
            command=self.cancel_optimization,
            state=tk.DISABLED
        )
        self.cancel_btn.pack(side=tk.RIGHT)
    
    def create_logs_tab(self):
        """Create the logs tab"""
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="Logs")
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(
            tab, 
            wrap=tk.WORD,
            font=('Consolas', 9),
            bg='#1e1e1e',
            fg='#ffffff',
            insertbackground='white'
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.insert(tk.END, "Logs will appear here...\n")
    
    def run_optimizations(self):
        """Run the selected optimizations"""
        level = self.optimization_level.get()
        create_backup = self.create_backup.get()
        
        # Update UI
        self.optimize_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL)
        self.update_status(f"Running {level} optimizations...")
        
        # Run in a separate thread
        threading.Thread(
            target=self._run_optimizations,
            args=(level, create_backup),
            daemon=True
        ).start()
    
    def _run_optimizations(self, level, create_backup):
        """Thread function to run optimizations"""
        try:
            # Get optimizer
            optimizer_map = {
                'safe': SafeOptimizer(OptimizationLevel.SAFE),
                'optional': OptionalOptimizer(OptimizationLevel.OPTIONAL),
                'hardcore': HardcoreOptimizer(OptimizationLevel.HARDCORE)
            }
            
            optimizer = optimizer_map.get(level, SafeOptimizer(OptimizationLevel.SAFE))
            
            # Create backup if needed
            if create_backup:
                self.log("Creating backup...")
                backup_data = {"optimization_level": level}
                backup_file = self.backup_manager.create_backup(backup_data, f"pre_{level}")
                self.log(f"Backup created: {backup_file}")
            
            # Run optimizations
            self.log(f"Starting {level} optimizations...")
            results = optimizer.run_all()
            
            # Show results
            success = sum(1 for r in results.values() if r)
            self.log(f"Complete! {success} of {len(results)} tasks successful.")
            self.update_status("Optimization complete!")
            
        except Exception as e:
            self.log(f"Error: {str(e)}", "error")
            self.update_status("Optimization failed!", error=True)
        finally:
            self.root.after(0, self.on_optimization_complete)
    
    def on_optimization_complete(self):
        """Clean up after optimization"""
        self.optimize_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.DISABLED)
    
    def cancel_optimization(self):
        """Cancel the running optimization"""
        if messagebox.askyesno("Cancel", "Are you sure you want to cancel?"):
            self.update_status("Cancelled by user")
            self.log("Optimization cancelled by user")
    
    def log(self, message, level="info"):
        """Add a message to the log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def update_status(self, message, error=False):
        """Update the status bar"""
        self.status_var.set(message)
        if error:
            self.log(f"Error: {message}", "error")
        self.root.update_idletasks()

def main():
    """Start the GUI application"""
    root = tk.Tk()
    app = RuddibabaOptimizerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
