"""
Optional optimization tasks that are generally safe but may affect some applications
"""
import os
import winreg
from typing import Optional

from . import BaseOptimizer, OptimizationLevel, OptimizationTask

class OptionalOptimizer(BaseOptimizer):
    """Optional optimizations that are generally safe but may affect some applications"""
    
    def _setup_tasks(self):
        """Initialize optional optimization tasks"""
        self.tasks = [
            OptimizationTask(
                name="disable_game_bar",
                description="Disable Xbox Game Bar",
                function=self.disable_game_bar,
                level=OptimizationLevel.OPTIONAL,
                requires_admin=True
            ),
            OptimizationTask(
                name="disable_telemetry",
                description="Disable telemetry and data collection",
                function=self.disable_telemetry,
                level=OptimizationLevel.OPTIONAL,
                requires_admin=True
            ),
            OptimizationTask(
                name="optimize_visual_effects",
                description="Optimize visual effects for better performance",
                function=self.optimize_visual_effects,
                level=OptimizationLevel.OPTIONAL,
                requires_admin=True
            )
        ]
    
    def disable_game_bar(self) -> None:
        """Disable Xbox Game Bar"""
        try:
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, 
                                r"SOFTWARE\Microsoft\Windows\CurrentVersion\GameDVR") as key:
                winreg.SetValueEx(key, "AppCaptureEnabled", 0, winreg.REG_DWORD, 0)
                winreg.SetValueEx(key, "GameDVR_Enabled", 0, winreg.REG_DWORD, 0)
        except WindowsError:
            pass
    
    def disable_telemetry(self) -> None:
        """Disable telemetry and data collection"""
        try:
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, 
                                r"SOFTWARE\Policies\Microsoft\Windows\DataCollection") as key:
                winreg.SetValueEx(key, "AllowTelemetry", 0, winreg.REG_DWORD, 0)
        except WindowsError:
            pass
    
    def optimize_visual_effects(self) -> None:
        """Optimize visual effects for better performance"""
        try:
            # Set visual effects to best performance
            os.system('powercfg -setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c')
            os.system('powercfg -change monitor-timeout-ac 0')
            os.system('powercfg -change monitor-timeout-dc 0')
        except Exception:
            pass
