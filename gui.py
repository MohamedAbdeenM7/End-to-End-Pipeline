import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SimpleDataGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Data Pipeline GUI")
        self.root.geometry("800x600")
        
        self.data = None
        
        # Create main layout
        self.create_widgets()
        
    def create_widgets(self):
        # Top Frame - Load Data
        top_frame = ttk.LabelFrame(self.root, text="Load Data", padding=10)
        top_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(top_frame, text="📁 Load CSV", 
                  command=self.load_csv, width=15).pack(side="left", padx=5)
        ttk.Button(top_frame, text="📁 Load Excel", 
                  command=self.load_excel, width=15).pack(side="left", padx=5)
        
        # Middle Frame - Notebook (Tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Tab 1: Data Preview
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Data Preview")
        
        # Treeview for data display
        self.tree = ttk.Treeview(self.tab1)
        scrollbar = ttk.Scrollbar(self.tab1, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Tab 2: Overview
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="Overview")
        
        self.overview_text = tk.Text(self.tab2, height=20, width=80)
        overview_scroll = ttk.Scrollbar(self.tab2, command=self.overview_text.yview)
        self.overview_text.configure(yscrollcommand=overview_scroll.set)
        
        self.overview_text.pack(side="left", fill="both", expand=True)
        overview_scroll.pack(side="right", fill="y")
        
        # Bottom Frame - Actions
        bottom_frame = ttk.LabelFrame(self.root, text="Quick Actions", padding=10)
        bottom_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(bottom_frame, text="🧹 Clean Data", 
                  command=self.clean_data, width=15).pack(side="left", padx=5)
        ttk.Button(bottom_frame, text="📊 Show Stats", 
                  command=self.show_stats, width=15).pack(side="left", padx=5)
        ttk.Button(bottom_frame, text="📈 Plot Histogram", 
                  command=self.plot_histogram, width=15).pack(side="left", padx=5)
        ttk.Button(bottom_frame, text="💾 Save Data", 
                  command=self.save_data, width=15).pack(side="left", padx=5)
        
        # Status Bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                              relief="sunken", anchor="w")
        status_bar.pack(fill="x", padx=10, pady=(0, 5))
    
    def load_csv(self):
        file_path = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.status_var.set(f"Loading {file_path}...")
                self.root.update()
                
                self.data = pd.read_csv(file_path)
                self.display_data()
                self.status_var.set(f"Loaded: {file_path} | Shape: {self.data.shape}")
                messagebox.showinfo("Success", f"Data loaded successfully!\nShape: {self.data.shape}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load CSV: {str(e)}")
                self.status_var.set("Error loading file")
    
    def load_excel(self):
        file_path = filedialog.askopenfilename(
            title="Select Excel file",
            filetypes=[("Excel files", "*.xlsx;*.xls"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.status_var.set(f"Loading {file_path}...")
                self.root.update()
                
                self.data = pd.read_excel(file_path)
                self.display_data()
                self.status_var.set(f"Loaded: {file_path} | Shape: {self.data.shape}")
                messagebox.showinfo("Success", f"Data loaded successfully!\nShape: {self.data.shape}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load Excel: {str(e)}")
                self.status_var.set("Error loading file")
    
    def display_data(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.tree["columns"] = []
        
        if self.data is not None:
            # Set up columns
            self.tree["columns"] = list(self.data.columns)
            self.tree.column("#0", width=0, stretch=False)  # Hide first column
            
            # Create headings
            for col in self.data.columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=100)
            
            # Add data (first 100 rows for performance)
            sample_data = self.data.head(100)
            for i, row in sample_data.iterrows():
                values = [str(val) for val in row.tolist()]
                self.tree.insert("", "end", values=values)
            
            # Update overview tab
            self.update_overview()
    
    def update_overview(self):
        if self.data is not None:
            overview_info = []
            overview_info.append(f"Data Shape: {self.data.shape[0]} rows × {self.data.shape[1]} columns\n")
            
            overview_info.append("Column Overview:")
            overview_info.append("-" * 50)
            
            for col in self.data.columns:
                dtype = self.data[col].dtype
                null_count = self.data[col].isnull().sum()
                null_percent = (null_count / len(self.data)) * 100
                unique_count = self.data[col].nunique()
                
                overview_info.append(
                    f"{col}: {dtype} | Nulls: {null_count} ({null_percent:.1f}%) | Unique: {unique_count}"
                )
            
            self.overview_text.delete(1.0, tk.END)
            self.overview_text.insert(1.0, "\n".join(overview_info))
    
    def clean_data(self):
        if self.data is None:
            messagebox.showwarning("No Data", "Please load data first!")
            return
        
        # Simple cleaning dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Clean Data")
        dialog.geometry("400x300")
        
        ttk.Label(dialog, text="Select cleaning operations:").pack(pady=10)
        
        # Checkboxes for cleaning options
        remove_nulls_var = tk.BooleanVar()
        remove_dups_var = tk.BooleanVar()
        fill_nulls_var = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(dialog, text="Remove rows with null values", 
                       variable=remove_nulls_var).pack(anchor="w", padx=20)
        ttk.Checkbutton(dialog, text="Remove duplicate rows", 
                       variable=remove_dups_var).pack(anchor="w", padx=20)
        ttk.Checkbutton(dialog, text="Fill nulls with 0", 
                       variable=fill_nulls_var).pack(anchor="w", padx=20)
        
        ttk.Label(dialog, text="\nSelect columns (leave empty for all):").pack(pady=10)
        columns_entry = ttk.Entry(dialog, width=40)
        columns_entry.pack(padx=20)
        
        def apply_cleaning():
            original_shape = self.data.shape
            
            try:
                # Apply cleaning operations
                if remove_nulls_var.get():
                    cols = [c.strip() for c in columns_entry.get().split(",")] if columns_entry.get() else None
                    self.data = self.data.dropna(subset=cols) if cols else self.data.dropna()
                
                if remove_dups_var.get():
                    self.data = self.data.drop_duplicates()
                
                if fill_nulls_var.get():
                    self.data = self.data.fillna(0)
                
                self.display_data()
                new_shape = self.data.shape
                
                messagebox.showinfo("Success", 
                    f"Data cleaned!\n\n"
                    f"Original: {original_shape[0]} rows × {original_shape[1]} cols\n"
                    f"Cleaned:  {new_shape[0]} rows × {new_shape[1]} cols\n"
                    f"Rows removed: {original_shape[0] - new_shape[0]}")
                
                dialog.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", f"Cleaning failed: {str(e)}")
        
        ttk.Button(dialog, text="Apply Cleaning", command=apply_cleaning).pack(pady=20)
        ttk.Button(dialog, text="Cancel", command=dialog.destroy).pack()
    
    def show_stats(self):
        if self.data is None:
            messagebox.showwarning("No Data", "Please load data first!")
            return
        
        # Show statistics in a new window
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Data Statistics")
        stats_window.geometry("500x400")
        
        # Text widget for stats
        stats_text = tk.Text(stats_window, wrap="none")
        scrollbar = ttk.Scrollbar(stats_window, orient="vertical", command=stats_text.yview)
        stats_text.configure(yscrollcommand=scrollbar.set)
        
        stats_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Generate stats
        stats_lines = ["DATA STATISTICS", "=" * 50, ""]
        
        # Numeric columns
        numeric_cols = self.data.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            stats_lines.append("NUMERIC COLUMNS:")
            stats_lines.append("-" * 40)
            
            stats = self.data[numeric_cols].describe()
            for col in numeric_cols:
                stats_lines.append(f"\n{col}:")
                stats_lines.append(f"  Mean: {self.data[col].mean():.2f}")
                stats_lines.append(f"  Std:  {self.data[col].std():.2f}")
                stats_lines.append(f"  Min:  {self.data[col].min():.2f}")
                stats_lines.append(f"  Max:  {self.data[col].max():.2f}")
                stats_lines.append(f"  Nulls: {self.data[col].isnull().sum()}")
        
        # Text columns
        text_cols = self.data.select_dtypes(include=['object']).columns
        if len(text_cols) > 0:
            stats_lines.append("\n\nTEXT COLUMNS:")
            stats_lines.append("-" * 40)
            
            for col in text_cols:
                stats_lines.append(f"\n{col}:")
                stats_lines.append(f"  Unique values: {self.data[col].nunique()}")
                stats_lines.append(f"  Most common: {self.data[col].mode().iloc[0] if not self.data[col].mode().empty else 'N/A'}")
                stats_lines.append(f"  Nulls: {self.data[col].isnull().sum()}")
        
        stats_text.insert(1.0, "\n".join(stats_lines))
        stats_text.configure(state="disabled")
    
    def plot_histogram(self):
        if self.data is None:
            messagebox.showwarning("No Data", "Please load data first!")
            return
        
        # Get numeric columns
        numeric_cols = self.data.select_dtypes(include=['number']).columns
        
        if len(numeric_cols) == 0:
            messagebox.showwarning("No Numeric Data", "No numeric columns to plot!")
            return
        
        # Let user select column
        selection_dialog = tk.Toplevel(self.root)
        selection_dialog.title("Select Column for Histogram")
        selection_dialog.geometry("300x200")
        
        ttk.Label(selection_dialog, text="Choose a numeric column:").pack(pady=10)
        
        selected_col = tk.StringVar(value=numeric_cols[0])
        
        for col in numeric_cols:
            ttk.Radiobutton(selection_dialog, text=col, 
                           variable=selected_col, value=col).pack(anchor="w", padx=20)
        
        def create_plot():
            col = selected_col.get()
            selection_dialog.destroy()
            
            # Create plot window
            plot_window = tk.Toplevel(self.root)
            plot_window.title(f"Histogram: {col}")
            plot_window.geometry("600x500")
            
            # Create figure
            fig, ax = plt.subplots(figsize=(6, 4))
            self.data[col].dropna().hist(ax=ax, bins=20, edgecolor='black')
            ax.set_title(f'Histogram of {col}')
            ax.set_xlabel(col)
            ax.set_ylabel('Frequency')
            
            # Embed in tkinter
            canvas = FigureCanvasTkAgg(fig, master=plot_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            # Add stats
            stats_text = f"""
            Statistics for {col}:
            Mean: {self.data[col].mean():.2f}
            Std:  {self.data[col].std():.2f}
            Min:  {self.data[col].min():.2f}
            Max:  {self.data[col].max():.2f}
            Nulls: {self.data[col].isnull().sum()}
            """
            ttk.Label(plot_window, text=stats_text).pack()
        
        ttk.Button(selection_dialog, text="Create Plot", command=create_plot).pack(pady=20)
    
    def save_data(self):
        if self.data is None:
            messagebox.showwarning("No Data", "No data to save!")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Data",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.status_var.set("Saving data...")
                self.root.update()
                
                if file_path.endswith('.csv'):
                    self.data.to_csv(file_path, index=False)
                elif file_path.endswith('.xlsx'):
                    self.data.to_excel(file_path, index=False)
                else:
                    self.data.to_csv(file_path, index=False)
                
                self.status_var.set(f"Data saved to: {file_path}")
                messagebox.showinfo("Success", f"Data saved successfully to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save data: {str(e)}")
                self.status_var.set("Error saving file")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleDataGUI(root)
    root.mainloop()