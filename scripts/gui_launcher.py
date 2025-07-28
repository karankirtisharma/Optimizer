"""
Launcher for the Ruddibaba Optimizer GUI
"""
import os
import sys
import subprocess

def main():
    """Launch the GUI with the correct Python environment"""
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    src_dir = os.path.join(project_root, 'src')
    
    # Add src directory to Python path
    sys.path.insert(0, src_dir)
    
    try:
        # Import and run the GUI directly
        from ui.gui import RuddibabaOptimizerGUI
        import tkinter as tk
        
        root = tk.Tk()
        app = RuddibabaOptimizerGUI(root)
        root.mainloop()
        
    except ImportError as e:
        print(f"Error: {e}")
        print("Make sure you have installed all dependencies from requirements.txt")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"Failed to start GUI: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
