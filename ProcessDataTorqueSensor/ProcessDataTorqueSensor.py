import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np
from scipy.stats import linregress, zscore
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class LinearRegressionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Linear Regression App")
        
        self.file_label = tk.Label(self.root, text="Select CSV File:")
        self.file_label.pack(pady=10)
        
        self.file_button = tk.Button(self.root, text="Browse", command=self.load_csv)
        self.file_button.pack()
        
        self.x_label = tk.Label(self.root, text="Select X Column:")
        self.x_label.pack(pady=10)
        
        self.x_var = tk.StringVar(self.root)
        self.x_dropdown = tk.OptionMenu(self.root, self.x_var, "")
        self.x_dropdown.pack()
        
        self.y_label = tk.Label(self.root, text="Select Y Column:")
        self.y_label.pack(pady=10)
        
        self.y_var = tk.StringVar(self.root)
        self.y_dropdown = tk.OptionMenu(self.root, self.y_var, "")
        self.y_dropdown.pack()
        
        self.calculate_button = tk.Button(self.root, text="Calculate Linear Regression", command=self.calculate_regression)
        self.calculate_button.pack(pady=20)
        
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack()
        
    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.data = pd.read_csv(file_path)
            self.update_dropdowns()
    
    def update_dropdowns(self):
        columns = self.data.columns.tolist()
        self.x_dropdown['menu'].delete(0, 'end')
        self.y_dropdown['menu'].delete(0, 'end')
        
        for col in columns:
            self.x_dropdown['menu'].add_command(label=col, command=lambda value=col: self.x_var.set(value))
            self.y_dropdown['menu'].add_command(label=col, command=lambda value=col: self.y_var.set(value))
    
    def calculate_regression(self):
        x_col = self.x_var.get()
        y_col = self.y_var.get()
        
        x_data = self.data[x_col]
        y_data = self.data[y_col]
        
        # Remove outliers using Z-score method
        z_scores = zscore(y_data)
        threshold = 10  # Adjust this threshold as needed
        y_data = y_data[abs(z_scores) < threshold]
        x_data = x_data[abs(z_scores) < threshold]
        
        slope, intercept, r_value, p_value, std_err = linregress(x_data, y_data)
        
        self.ax.clear()
        self.ax.scatter(x_data, y_data, label="Data")
        self.ax.plot(x_data, slope * x_data + intercept, color='red', label="Linear Regression")
        self.ax.set_xlabel(x_col)
        self.ax.set_ylabel(y_col)
        self.ax.legend()

        equation = f"Equation: y = {slope:.4f}x + {intercept:.4f}"
        self.equation_label = tk.Label(self.root, text=equation)
        self.equation_label.pack(pady=10)
        
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = LinearRegressionApp(root)
    root.mainloop()
