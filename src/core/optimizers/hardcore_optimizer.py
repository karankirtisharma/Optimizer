"""
Hardcore optimization tasks that provide maximum performance but may affect system stability
"""
import os
import winreg
from typing import Optional

from . import BaseOptimizer, OptimizationLevel, OptimizationTask

class HardcoreOptimizer(BaseOptimizer):
    """Hardcore optimizations for maximum performance (use with caution)"""
    
    def _setup_tasks(self):
        """Initialize hardcore optimization tasks"""
        self.tasks = [
            OptimizationTask(
                name="disable_superfetch",
                description="Disable Superfetch service",
                function=self.disable_superfetch,
                level=OptimizationLevel.HARDCORE,
                requires_admin=True
            ),
            OptimizationTask(
                name="disable_search_indexing",
                description="Disable Windows Search indexing",
                function=self.disable_search_indexing,
                level=OptimizationLevel.HARDCORE,
                requires_admin=True
            ),
            OptimizationTask(
                name="optimize_network_settings",
                description="Optimize network settings for performance",
                function=self.optimize_network_settings,
                level=OptimizationLevel.HARDCORE,
                requires_admin=True
            )
        ]
    
    def disable_superfetch(self) -> None:
        """Disable Superfetch service"""
        try:
            # Stop and disable Superfetch service
            os.system('net stop "SysMain"')
            os.system('sc config "SysMain" start= disabled')
            
            # Disable Superfetch in registry
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, 
                                r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters") as key:
                winreg.SetValueEx(key, "EnableSuperfetch", 0, winreg.REG_DWORD, 0)
                winreg.SetValueEx(key, "EnablePrefetcher", 0, winreg.REG_DWORD, 0)
        except WindowsError:
            pass
    
    def disable_search_indexing(self) -> None:
        """Disable Windows Search indexing"""
        try:
            # Stop and disable Windows Search service
            os.system('net stop "WSearch"')
            os.system('sc config "WSearch" start= disabled')
            
            # Disable indexing in registry
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, 
                                r"SOFTWARE\Policies\Microsoft\Windows\Windows Search") as key:
                winreg.SetValueEx(key, "DisableBackoff", 0, winreg.REG_DWORD, 1)
                winreg.SetValueEx(key, "DisableRemovableDriveIndexing", 0, winreg.REG_DWORD, 1)
                winreg.SetValueEx(key, "PreventIndexingLowDiskSpaceMB", 0, winreg.REG_DWORD, 1)
        except WindowsError:
            pass
    
    def optimize_network_settings(self) -> None:
        """Optimize network settings for performance"""
        try:
            # Optimize TCP settings
            os.system('netsh int tcp set global autotuninglevel=restricted')
            os.system('netsh int tcp set global chimney=auto')
            os.system('netsh int tcp set global dca=enabled')
            os.system('netsh int tcp set global netdma=enabled')
            os.system('netsh int tcp set global rss=enabled')
            
            # Disable network throttling
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, 
                                r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile") as key:
                winreg.SetValueEx(key, "NetworkThrottlingIndex", 0, winreg.REG_DWORD, 0xFFFFFFFF)
        except Exception:
            pass
