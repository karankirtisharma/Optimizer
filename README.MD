## Computer Spec Optimizer

A powerful Windows optimization tool with multiple optimization levels, built with Python, Typer, and Rich.

![Ruddibaba Optimizer](https://img.shields.io/badge/Status-Alpha-yellow)
![Python Version](https://img.shields.io/badge/Python-3.7%2B-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

## Features

- 🚀 Three optimization levels: Safe, Optional, and Hardcore
- 🎨 Beautiful terminal interface with Rich
- 🔒 Automatic backup and restore functionality
- 📊 Detailed logging and progress tracking
- 🛠️ Modular design for easy extension
- 💻 Cross-version Python support (3.7+)
- 🔄 PowerShell and Batch script integration

## Installation

### Prerequisites

- Python 3.7 or higher
- Windows 10/11 (64-bit)
- Administrator privileges (for some optimizations)

### Using pip

```bash
pip install -e .
```

### Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ruddibaba-optimizer.git
   cd ruddibaba-optimizer
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Usage

### Basic Commands

```bash
# Show help
ruddibaba-optimizer --help

# Run safe optimizations
ruddibaba-optimizer optimize run --level safe

# Run optional optimizations (with admin privileges)
ruddibaba-optimizer optimize run --level optional

# Run hardcore optimizations (use with caution!)
ruddibaba-optimizer optimize run --level hardcore

# List all available optimizations
ruddibaba-optimizer optimize list
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `-l`, `--level` | Optimization level: safe, optional, hardcore (default: safe) |
| `--no-backup` | Skip creating a backup before making changes |
| `-f`, `--force` | Run without confirmation |
| `--verbose` | Enable verbose output |

## Optimization Levels

### Safe
- Cleans temporary files
- Optimizes power settings
- Disables unnecessary startup programs

### Optional
- Disables telemetry
- Optimizes visual effects
- Disables Xbox Game Bar

### Hardcore (Use with caution!)
- Disables Superfetch
- Disables Windows Search indexing
- Optimizes network settings
- Applies aggressive power optimizations

## Building from Source

### Create Executable

```bash
pip install pyinstaller
pyinstaller --onefile --name ruddibaba-optimizer src/ruddibaba_optimizer/cli.py
```

### Create Installer

```bash
pip install nsis
python setup.py bdist_nsis
```

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Typer](https://typer.tiangolo.com/) - For building great CLIs
- [Rich](https://github.com/Textualize/rich) - For beautiful terminal output
- [PyInstaller](https://www.pyinstaller.org/) - For packaging Python applications

## Disclaimer

This software is provided "as is" without any warranties. Use at your own risk. The author is not responsible for any damage or data loss caused by using this software. Always create backups before making system changes.
