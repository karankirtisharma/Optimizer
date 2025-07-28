"""
Backup and restore functionality for Ruddibaba Optimizer
"""
import os
import json
import shutil
import tempfile
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import winreg

class BackupManager:
    """Manages backup and restore operations for system optimizations"""
    
    def __init__(self, backup_dir: Optional[str] = None):
        """Initialize the backup manager"""
        self.logger = logging.getLogger(__name__)
        self.backup_dir = backup_dir or os.path.join(
            os.environ.get('LOCALAPPDATA', ''),
            'RuddibabaOptimizer',
            'backups'
        )
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def create_backup(self, backup_data: Dict[str, Any], backup_name: str) -> str:
        """
        Create a backup of the current system state
        
        Args:
            backup_data: Dictionary containing data to back up
            backup_name: Name for the backup
            
        Returns:
            Path to the created backup file
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(self.backup_dir, f"{backup_name}_{timestamp}.json")
            
            with open(backup_file, 'w') as f:
                json.dump(backup_data, f, indent=2)
                
            self.logger.info(f"Created backup at: {backup_file}")
            return backup_file
            
        except Exception as e:
            self.logger.error(f"Failed to create backup: {str(e)}")
            raise
    
    def restore_backup(self, backup_file: str) -> bool:
        """
        Restore system state from a backup file
        
        Args:
            backup_file: Path to the backup file to restore from
            
        Returns:
            bool: True if restore was successful, False otherwise
        """
        try:
            if not os.path.exists(backup_file):
                self.logger.error(f"Backup file not found: {backup_file}")
                return False
                
            with open(backup_file, 'r') as f:
                backup_data = json.load(f)
            
            self.logger.info(f"Restoring from backup: {backup_file}")
            
            # Restore registry values
            if 'registry' in backup_data:
                self._restore_registry(backup_data['registry'])
                
            # Restore files
            if 'files' in backup_data:
                self._restore_files(backup_data['files'])
                
            self.logger.info("Backup restore completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to restore backup: {str(e)}")
            return False
    
    def _restore_registry(self, registry_data: Dict[str, Any]) -> None:
        """Restore registry values from backup"""
        for key_path, values in registry_data.items():
            try:
                # Handle different registry hives
                if key_path.startswith('HKCU'):
                    hive = winreg.HKEY_CURRENT_USER
                    sub_key = key_path[5:]  # Remove 'HKCU\' prefix
                elif key_path.startswith('HKLM'):
                    hive = winreg.HKEY_LOCAL_MACHINE
                    sub_key = key_path[5:]  # Remove 'HKLM\' prefix
                else:
                    self.logger.warning(f"Unsupported registry hive in {key_path}")
                    continue
                
                # Create or open the registry key
                with winreg.CreateKey(hive, sub_key) as key:
                    for value_name, (value_type, value_data) in values.items():
                        winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                        
            except Exception as e:
                self.logger.error(f"Failed to restore registry key {key_path}: {str(e)}")
    
    def _restore_files(self, files_data: Dict[str, str]) -> None:
        """Restore files from backup"""
        for dest_path, source_path in files_data.items():
            try:
                if os.path.exists(source_path):
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    shutil.copy2(source_path, dest_path)
            except Exception as e:
                self.logger.error(f"Failed to restore file {dest_path}: {str(e)}")
