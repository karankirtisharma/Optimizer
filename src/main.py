"""
Ruddibaba Optimizer - Main entry point
"""
import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .ui.console import setup_console
from .ui.branding import get_ascii_logo

# Initialize the Typer app
app = typer.Typer(
    name="ruddibaba-optimizer",
    help="A powerful Windows optimization tool with multiple optimization levels",
    add_completion=False,
)

# Global console instance
console = setup_console()

@app.callback()
def main():
    """Ruddibaba Optimizer - Optimize your Windows experience"""
    # Display the ASCII logo
    console.print(Panel(
        Text(get_ascii_logo(), style="bold blue"),
        border_style="blue",
        expand=False,
    ))

@app.command()
def version():
    """Show the version of Ruddibaba Optimizer"""
    from ruddibaba_optimizer import __version__
    console.print(f"Ruddibaba Optimizer v{__version__}")

if __name__ == "__main__":
    app()
