"""
Optimization commands for Ruddibaba Optimizer
"""
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from ..core import (
    SafeOptimizer, 
    OptionalOptimizer, 
    HardcoreOptimizer,
    OptimizationLevel
)
from ..core.logger import setup_logging
from ..core.backup import BackupManager
from ..ui.console import console

# Create Typer app
app = typer.Typer(name="optimize", help="Run optimization tasks")

# Initialize logger
logger = setup_logging().get_logger(__name__)

# Initialize backup manager
backup_manager = BackupManager()

def get_optimizer(level: OptimizationLevel):
    """Get the appropriate optimizer for the given level"""
    optimizers = {
        OptimizationLevel.SAFE: SafeOptimizer,
        OptimizationLevel.OPTIONAL: OptionalOptimizer,
        OptimizationLevel.HARDCORE: HardcoreOptimizer
    }
    return optimizers[level](level=level)

def display_optimization_plan(optimizer) -> None:
    """Display the optimization plan to the user"""
    tasks = optimizer.get_available_tasks()
    
    if not tasks:
        console.print("[yellow]No optimization tasks available for the selected level.[/]")
        return False
    
    table = Table(title="Optimization Plan", show_header=True, header_style="bold magenta")
    table.add_column("Task", style="cyan")
    table.add_column("Description")
    table.add_column("Requires Admin", justify="center")
    
    for task in tasks:
        table.add_row(
            task.name,
            task.description,
            "✓" if task.requires_admin else ""
        )
    
    console.print(Panel(table, title="Optimization Plan", border_style="blue"))
    return True

@app.command()
def run(
    level: str = typer.Option(
        "safe", 
        "--level", "-l", 
        help="Optimization level: safe, optional, or hardcore"
    ),
    backup: bool = typer.Option(
        True, 
        help="Create a backup before making changes"
    ),
    force: bool = typer.Option(
        False, 
        "--force", "-f", 
        help="Run without confirmation"
    )
):
    """Run optimization tasks at the specified level"""
    try:
        # Convert level string to enum
        try:
            opt_level = OptimizationLevel[level.upper()]
        except KeyError:
            console.print(f"[red]Error: Invalid optimization level '{level}'. Must be one of: safe, optional, hardcore[/]")
            raise typer.Exit(1)
        
        # Get the appropriate optimizer
        optimizer = get_optimizer(opt_level)
        
        # Display optimization plan
        console.print(f"[bold]Optimization Level:[/] [cyan]{opt_level.name.title()}[/]")
        
        if not display_optimization_plan(optimizer):
            return
        
        # Ask for confirmation
        if not force:
            console.print("\n[bold yellow]WARNING:[/] These changes may affect system stability.\n")
            confirm = typer.confirm("Do you want to proceed with the optimization?")
            if not confirm:
                console.print("[yellow]Optimization cancelled.[/]")
                return
        
        # Create backup if requested
        backup_file = None
        if backup:
            with console.status("Creating backup...", spinner="dots"):
                try:
                    # TODO: Implement actual backup of system state
                    backup_data = {"optimization_level": level, "tasks": []}
                    backup_file = backup_manager.create_backup(backup_data, f"pre_optimization_{level}")
                    console.print(f"[green]✓ Backup created: {backup_file}[/]")
                except Exception as e:
                    console.print(f"[red]Failed to create backup: {str(e)}[/]")
                    if not typer.confirm("Continue without backup?"):
                        return
        
        # Run optimizations
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            task = progress.add_task("Running optimizations...", total=len(optimizer.get_available_tasks()))
            
            def progress_callback():
                progress.advance(task)
            
            # Run the optimizer with progress updates
            results = optimizer.run_all(progress_callback=progress_callback)
        
        # Display results
        success_count = sum(1 for r in results.values() if r)
        total_count = len(results)
        
        console.print(f"\n[bold]Optimization Complete![/]")
        console.print(f"[green]✓ {success_count} of {total_count} tasks completed successfully[/]")
        
        if backup_file:
            console.print(f"\n[dim]Backup saved to: {backup_file}[/]")
        
    except Exception as e:
        logger.exception("Error during optimization")
        console.print(f"[red]Error: {str(e)}[/]")
        raise typer.Exit(1)

@app.command()
def list():
    """List all available optimization tasks by level"""
    for level in OptimizationLevel:
        optimizer = get_optimizer(level)
        console.print(f"\n[bold magenta]=== {level.name.title()} Optimizations ===[/]")
        display_optimization_plan(optimizer)

if __name__ == "__main__":
    app()
