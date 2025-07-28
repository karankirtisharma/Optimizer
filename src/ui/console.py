"""
Console setup and configuration for Ruddibaba Optimizer
"""
from rich.console import Console
from rich.theme import Theme

def setup_console() -> Console:
    """
    Configure and return a Rich Console instance with custom styling
    """
    custom_theme = Theme({
        "success": "bold green",
        "warning": "bold yellow",
        "error": "bold red",
        "info": "bold blue",
        "title": "bold cyan",
        "subtitle": "bold magenta",
        "prompt": "bold yellow",
    })
    
    return Console(
        theme=custom_theme,
        highlight=False,
        soft_wrap=True,
        color_system="auto"
    )
