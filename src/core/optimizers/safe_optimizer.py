"""
Safe optimization tasks that are generally safe for all systems
"""
import os
import shutil
import tempfile
from pathlib import Path
from typing import List, Optional
import winreg

from . import BaseOptimizer, OptimizationLevel, OptimizationTask

class SafeOptimizer(BaseOptimizer):
    """Safe optimizations that are generally safe for all systems"""
    
    def _setup_tasks(self):
        """Initialize safe optimization tasks"""
        self.tasks = [
            OptimizationTask(
                name="clear_temp_files",
                description="Clear temporary files",
                function=self.clear_temp_files,
                level=OptimizationLevel.SAFE
            ),
            OptimizationTask(
                name="clear_windows_update_cache",
                description="Clear Windows Update cache",
                function=self.clear_windows_update_cache,
                level=OptimizationLevel.SAFE,
                requires_admin=True
            ),
            OptimizationTask(
                name="optimize_power_settings",
                description="Optimize power settings for better performance",
                function=self.optimize_power_settings,
                level=OptimizationLevel.SAFE,
                requires_admin=True
            )
        ]
    
    def clear_temp_files(self) -> None:
        """Clear temporary files from common locations"""
        temp_dirs = [
            os.environ.get('TEMP', ''),
            os.environ.get('TMP', ''),
            os.path.join(os.environ.get('WINDIR', ''), 'Temp'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Temp')
        ]
        
        for temp_dir in temp_dirs:
            if temp_dir and os.path.isdir(temp_dir):
                try:
                    for item in os.listdir(temp_dir):
                        item_path = os.path.join(temp_dir, item)
                        try:
                            if os.path.isfile(item_path) or os.path.islink(item_path):
                                os.unlink(item_path)
                            elif os.path.isdir(item_path):
                                shutil.rmtree(item_path, ignore_errors=True)
                        except (OSError, shutil.Error):
                            continue
                except (OSError, PermissionError):
                    continue
    
    def clear_windows_update_cache(self) -> None:
        """Clear Windows Update cache"""
        update_cache_path = os.path.join(
            os.environ.get('WINDIR', ''), 
            'SoftwareDistribution', 
            'Download'
        )
        
        if os.path.exists(update_cache_path):
            try:
                shutil.rmtree(update_cache_path, ignore_errors=True)
                os.makedirs(update_cache_path, exist_ok=True)
            except (OSError, PermissionError):
                pass
    
    def optimize_power_settings(self) -> None:
        """Optimize power settings for better performance"""
        try:
            # Set power plan to High Performance
            os.system('powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c')
            # Disable USB selective suspend
            os.system('powercfg /setacvalueindex scheme_current 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0')
            # Set HDD to never turn off
            os.system('powercfg /change disk-timeout-ac 0')
            os.system('powercfg /change disk-timeout-dc 0')
        except Exception:
            pass
