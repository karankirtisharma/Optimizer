"""
Optimization modules for Ruddibaba Optimizer
"""
from enum import Enum, auto
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass
from pathlib import Path
import logging

class OptimizationLevel(Enum):
    """Optimization levels for the optimizer"""
    SAFE = auto()
    OPTIONAL = auto()
    HARDCORE = auto()

@dataclass
class OptimizationTask:
    """Represents a single optimization task"""
    name: str
    description: str
    function: Callable
    level: OptimizationLevel
    requires_admin: bool = False
    enabled: bool = True

class BaseOptimizer:
    """Base class for all optimizers"""
    
    def __init__(self, level: OptimizationLevel):
        self.level = level
        self.tasks: List[OptimizationTask] = []
        self.logger = logging.getLogger(__name__)
        self._setup_tasks()
    
    def _setup_tasks(self):
        """Setup optimization tasks. Should be implemented by subclasses."""
        pass
    
    def get_available_tasks(self) -> List[OptimizationTask]:
        """Get all available tasks for the current optimization level"""
        return [
            task for task in self.tasks 
            if task.level.value <= self.level.value and task.enabled
        ]
    
    def run_all(self) -> Dict[str, bool]:
        """Run all enabled tasks for the current optimization level"""
        results = {}
        for task in self.get_available_tasks():
            try:
                self.logger.info(f"Running task: {task.name}")
                task.function()
                results[task.name] = True
            except Exception as e:
                self.logger.error(f"Error running task {task.name}: {str(e)}")
                results[task.name] = False
        return results

# Import optimizers after base classes are defined
from .safe_optimizer import SafeOptimizer
from .optional_optimizer import OptionalOptimizer
from .hardcore_optimizer import HardcoreOptimizer

__all__ = [
    'OptimizationLevel',
    'OptimizationTask',
    'BaseOptimizer',
    'SafeOptimizer',
    'OptionalOptimizer',
    'HardcoreOptimizer'
]
