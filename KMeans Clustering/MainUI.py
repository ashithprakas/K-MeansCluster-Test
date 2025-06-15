import tkinter as tk
from tkinter import ttk
from RegularKMeansUI import RegularKMeansUI
from WeightedKMeansUI import WeightedKMeansUI
from EntropyKMeansUI import EntropyKMeansUI
import sys

class MainUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Clustering Methods")
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create buttons
        self.create_buttons()
        
        # Store current UI
        self.current_ui = None
        
        # Set up window close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_buttons(self):
        # Regular K-means button
        self.kmeans_btn = ttk.Button(
            self.main_frame, 
            text="Regular K-Means", 
            command=lambda: self.switch_ui("regular")
        )
        self.kmeans_btn.grid(row=0, column=0, padx=5, pady=5)
        
        # Weighted K-means button
        self.weighted_btn = ttk.Button(
            self.main_frame, 
            text="Weighted K-Means", 
            command=lambda: self.switch_ui("weighted")
        )
        self.weighted_btn.grid(row=0, column=1, padx=5, pady=5)
        
        # Entropy-based K-means button
        self.entropy_btn = ttk.Button(
            self.main_frame, 
            text="Entropy K-Means", 
            command=lambda: self.switch_ui("entropy")
        )
        self.entropy_btn.grid(row=0, column=2, padx=5, pady=5)

    def switch_ui(self, ui_type):
        # Clear current UI if it exists
        if self.current_ui is not None:
            self.current_ui.root.destroy()
        
        # Create new window for the selected UI
        new_window = tk.Toplevel(self.root)
        new_window.protocol("WM_DELETE_WINDOW", lambda: self.close_child_window(new_window))
        
        if ui_type == "regular":
            self.current_ui = RegularKMeansUI(new_window)
        elif ui_type == "weighted":
            self.current_ui = WeightedKMeansUI(new_window)
        else:  # entropy
            self.current_ui = EntropyKMeansUI(new_window)

    def close_child_window(self, window):
        """Handle closing of child windows"""
        if self.current_ui is not None:
            self.current_ui.root.destroy()
            self.current_ui = None
            # If main window is also closed, exit the application
            if not self.root.winfo_exists():
                sys.exit(0)

    def on_closing(self):
        """Handle main window closing"""
        # Close any open child windows
        if self.current_ui is not None:
            self.current_ui.root.destroy()
        
        # Close the main window
        self.root.destroy()
        # Exit the application
        sys.exit(0)

def main():
    root = tk.Tk()
    app = MainUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 