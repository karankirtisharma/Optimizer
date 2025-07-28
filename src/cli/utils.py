"""
Utility functions for Ruddibaba Optimizer CLI
"""
import os
import sys
import ctypes
import platform
from typing import Optional, List, Dict, Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def is_admin() -> bool:
    """Check if the script is running with administrator privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except AttributeError:
        return False

def check_requirements() -> bool:
    """Check system requirements"""
    # Check if running on Windows
    if platform.system() != 'Windows':
        console.print("[red]Error: This tool only works on Windows.[/]")
        return False
    
    # Check Python version (3.7+ required)
    if sys.version_info < (3, 7):
        console.print("[red]Error: Python 3.7 or higher is required.[/]")
        return False
    
    return True

def display_welcome() -> None:
    """Display welcome message and system information"""
    from .. import __version__
    from ..ui.branding import get_ascii_logo
    
    console.print(Panel(
        f"[bold blue]{get_ascii_logo()}[/]\n"
        f"[bold]Version:[/] {__version__}\n"
        f"[bold]System:[/] {platform.system()} {platform.version()}\n"
        f"[bold]Python:[/] {platform.python_version()}",
        title="Ruddibaba Optimizer",
        border_style="blue",
        expand=False
    ))

def display_summary(results: Dict[str, bool]) -> None:
    """Display a summary of optimization results"""
    if not results:
        console.print("[yellow]No optimizations were performed.[/]")
        return
    
    success_count = sum(1 for r in results.values() if r)
    total_count = len(results)
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Task", style="cyan")
    table.add_column("Status", justify="center")
    
    for task, success in results.items():
        status = "[green]✓ Success" if success else "[red]✗ Failed"
        table.add_row(task, status)
    
    console.print(Panel(
        table,
        title=f"Optimization Results ({success_count}/{total_count} successful)",
        border_style="green" if success_count == total_count else "yellow"
    ))

def prompt_restart() -> bool:
    """Prompt the user to restart the system"""
    console.print("\n[bold yellow]Some changes require a system restart to take effect.[/]")
    if console.input("Restart now? [y/N] ").lower() == 'y':
        try:
            import os
            os.system("shutdown /r /t 1")
            return True
        except Exception as e:
            console.print(f"[red]Failed to restart: {str(e)}[/]")
            return False
    return False
