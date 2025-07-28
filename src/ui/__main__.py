"""
Main entry point for the Ruddibaba Optimizer GUI
"""
import sys
from .gui import RuddibabaOptimizerGUI

def main():
    """Main function to run the GUI"""
    import tkinter as tk
    root = tk.Tk()
    app = RuddibabaOptimizerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
