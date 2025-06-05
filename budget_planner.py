import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Tuple
import random

class BudgetPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Planner - Knapsack Algorithms")
        self.root.geometry("1000x800")
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use clam theme as base
        
        # Configure colors and styles
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabelframe', background='#f0f0f0')
        self.style.configure('TLabelframe.Label', font=('Helvetica', 10, 'bold'), background='#f0f0f0')
        self.style.configure('TButton', font=('Helvetica', 9), padding=5)
        self.style.configure('TLabel', font=('Helvetica', 9), background='#f0f0f0')
        self.style.configure('Treeview', font=('Helvetica', 9), rowheight=25)
        self.style.configure('Treeview.Heading', font=('Helvetica', 9, 'bold'))
        
        # Items list to store (name, price, value) tuples
        self.items: List[Tuple[str, float, float]] = []
        
        # Algorithm selection
        self.algorithm_var = tk.StringVar(value="0/1")
        
        # Create main container with padding
        main_container = ttk.Frame(self.root, padding="10")
        main_container.pack(fill="both", expand=True)
        
        # Create widgets
        self.create_widgets(main_container)
        
    def create_widget(self, parent):
        # Input Frame with modern styling
        input_frame = ttk.LabelFrame(parent, text="Add Items", padding=15)
        input_frame.pack(fill="x", pady=(0, 10))
        
        # Create a grid layout for inputs
        input_grid = ttk.Frame(input_frame)
        input_grid.pack(fill="x", padx=5, pady=5)
        
        # Item name input with improved layout
        ttk.Label(input_grid, text="Item Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(input_grid, textvariable=self.name_var, width=20)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Price input
        ttk.Label(input_grid, text="Price ($):").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.price_var = tk.StringVar()
        price_entry = ttk.Entry(input_grid, textvariable=self.price_var, width=15)
        price_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Value input
        ttk.Label(input_grid, text="Value (Importance):").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.value_var = tk.StringVar()
        value_entry = ttk.Entry(input_grid, textvariable=self.value_var, width=15)
        value_entry.grid(row=0, column=5, padx=5, pady=5)
        
        # Add button with modern styling
        add_btn = ttk.Button(input_grid, text="Add Item", command=self.add_item, style='Accent.TButton')
        add_btn.grid(row=0, column=6, padx=5, pady=5)
        
        # Algorithm selection frame with improved layout
        algo_frame = ttk.LabelFrame(parent, text="Algorithm Selection", padding=15)
        algo_frame.pack(fill="x", pady=(0, 10))
        
        algo_container = ttk.Frame(algo_frame)
        algo_container.pack(fill="x", padx=5, pady=5)
        
        ttk.Radiobutton(algo_container, text="0/1 Knapsack (Items cannot be divided)", 
                       variable=self.algorithm_var, value="0/1").pack(side="left", padx=20)
        
        ttk.Radiobutton(algo_container, text="Fractional Knapsack (Items can be divided)", 
                       variable=self.algorithm_var, value="fractional").pack(side="left", padx=20)
        
        # Budget input with modern styling
        budget_frame = ttk.LabelFrame(parent, text="Budget", padding=15)
        budget_frame.pack(fill="x", pady=(0, 10))
        
        budget_container = ttk.Frame(budget_frame)
        budget_container.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(budget_container, text="Total Budget ($):").pack(side="left", padx=5)
        self.budget_var = tk.StringVar()
        budget_entry = ttk.Entry(budget_container, textvariable=self.budget_var, width=15)
        budget_entry.pack(side="left", padx=5)
        
        # Optimize button with modern styling
        self.optimize_btn = ttk.Button(budget_container, text="Optimize", command=self.optimize, style='Accent.TButton')
        self.optimize_btn.pack(side="left", padx=5)
        
        # Clear all button
        clear_btn = ttk.Button(budget_container, text="Clear All", command=self.clear_all)
        clear_btn.pack(side="left", padx=5)
        
        # Items list display with improved styling
        list_frame = ttk.LabelFrame(parent, text="Items List", padding=15)
        list_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Create Treeview with scrollbar and modern styling
        tree_frame = ttk.Frame(list_frame)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.tree = ttk.Treeview(tree_frame, columns=("Name", "Price", "Value", "Value/Price"), 
                                show="headings", style="Treeview")
        self.tree.heading("Name", text="Item Name")
        self.tree.heading("Price", text="Price ($)")
        self.tree.heading("Value", text="Value")
        self.tree.heading("Value/Price", text="Value/Price")
        
        # Configure column widths
        self.tree.column("Name", width=300)
        self.tree.column("Price", width=150)
        self.tree.column("Value", width=150)
        self.tree.column("Value/Price", width=150)
        
        # Add scrollbar with modern styling
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind double-click event
        self.tree.bind("<Double-1>", self.on_item_double_click)
        
        # Results display with improved styling
        result_frame = ttk.LabelFrame(parent, text="Results", padding=15)
        result_frame.pack(fill="x", pady=(0, 10))
        
        self.result_text = tk.Text(result_frame, height=8, wrap=tk.WORD, font=('Helvetica', 9))
        self.result_text.pack(fill="x", padx=5, pady=5)
        
        # Status bar with modern styling
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(parent, textvariable=self.status_var, relief="sunken", 
                             anchor="w", padding=(5, 2))
        status_bar.pack(fill="x")
        
        # Configure custom styles
        self.style.configure('Accent.TButton', 
                           background='#007bff',
                           foreground='white',
                           padding=5)
        
        # Set initial button state
        self.optimize_btn.state(["disabled"])
        
    def add_items(self):
        try:
            name = self.name_var.get().strip()
            if not name:
                messagebox.showerror("Error", "Please enter an item name")
                return
                
            price = float(self.price_var.get())
            value = float(self.value_var.get())
            
            if price <= 0 or value <= 0:
                messagebox.showerror("Error", "Price and value must be positive numbers")
                return
                
            self.items.append((name, price, value))
            
            # Calculate value/price ratio for display
            ratio = value / price
            
            self.tree.insert("", "end", values=(name, f"${price:.2f}", f"{value:.2f}", f"{ratio:.2f}"))
            
            # Clear input fields
            self.name_var.set("")
            self.price_var.set("")
            self.value_var.set("")
            
            # Update status
            self.status_var.set(f"Added item: {name}")
            
            # Enable optimize button if we have items
            self.optimize_btn.state(["!disabled"])
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for price and value")
    
    def on_item_double_click(self, event):
        item = self.tree.selection()[0]
        if messagebox.askyesno("Delete Item", "Do you want to delete this item?"):
            idx = self.tree.index(item)
            self.items.pop(idx)
            self.tree.delete(item)
            self.status_var.set("Item deleted")
            
            if not self.items:
                self.optimize_btn.state(["disabled"])
    
    def clear_all(self):
        if messagebox.askyesno("Clear All", "Are you sure you want to clear all items?"):
            self.items.clear()
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.result_text.delete(1.0, tk.END)
            self.optimize_btn.state(["disabled"])
            self.status_var.set("All items cleared")
    
    def knapsack_01(self, budget: float, items: List[Tuple[str, float, float]]) -> Tuple[List[int], float, float]:
        n = len(items)
        dp = [[0 for _ in range(int(budget) + 1)] for _ in range(n + 1)]
        selected = [[False for _ in range(int(budget) + 1)] for _ in range(n + 1)]
        
        # Fill dp table
        for i in range(1, n + 1):
            for w in range(int(budget) + 1):
                if items[i-1][1] <= w:  # items[i-1][1] is price
                    if items[i-1][2] + dp[i-1][w - int(items[i-1][1])] > dp[i-1][w]:  # items[i-1][2] is value
                        dp[i][w] = items[i-1][2] + dp[i-1][w - int(items[i-1][1])]
                        selected[i][w] = True
                    else:
                        dp[i][w] = dp[i-1][w]
                else:
                    dp[i][w] = dp[i-1][w]
        
        # Find selected items
        selected_items = []
        w = int(budget)
        total_cost = 0
        
        for i in range(n, 0, -1):
            if selected[i][w]:
                selected_items.append(i-1)
                w -= int(items[i-1][1])
                total_cost += items[i-1][1]
        
        return selected_items, total_cost, dp[n][int(budget)]
    
    def knapsack_fractional(self, budget: float, items: List[Tuple[str, float, float]]) -> Tuple[List[Tuple[int, float]], float, float]:
        # Calculate value/price ratio for each item
        ratios = [(i, items[i][2] / items[i][1]) for i in range(len(items))]
        
        # Sort by ratio in descending order
        ratios.sort(key=lambda x: x[1], reverse=True)
        
        selected_items = []
        total_cost = 0
        total_value = 0
        remaining_budget = budget
        
        for idx, ratio in ratios:
            name, price, value = items[idx]
            
            if remaining_budget >= price:
                # Take the whole item
                selected_items.append((idx, 1.0))
                total_cost += price
                total_value += value
                remaining_budget -= price
            else:
                # Take a fraction of the item
                fraction = remaining_budget / price
                selected_items.append((idx, fraction))
                total_cost += remaining_budget
                total_value += value * fraction
                remaining_budget = 0
                break
        
        return selected_items, total_cost, total_value
    
    def optimize(self):
        try:
            budget = float(self.budget_var.get())
            if budget <= 0:
                messagebox.showerror("Error", "Budget must be a positive number")
                return
                
            if not self.items:
                messagebox.showerror("Error", "Please add some items first")
                return
            
            algorithm = self.algorithm_var.get()
            
            if algorithm == "0/1":
                selected_indices, total_cost, total_value = self.knapsack_01(budget, self.items)
                
                # Display results
                result = "0/1 Knapsack Results:\n"
                result += "Selected Items:\n"
                for idx in selected_indices:
                    name, price, value = self.items[idx]
                    result += f"• {name}: Price=${price:.2f}, Value={value:.2f}\n"
                
                result += f"\nTotal Cost: ${total_cost:.2f}\n"
                result += f"Total Value: {total_value:.2f}\n"
                result += f"Remaining Budget: ${(budget - total_cost):.2f}"
                
            else:  # Fractional knapsack
                selected_items, total_cost, total_value = self.knapsack_fractional(budget, self.items)
                
                # Display results
                result = "Fractional Knapsack Results:\n"
                result += "Selected Items:\n"
                for idx, fraction in selected_items:
                    name, price, value = self.items[idx]
                    if fraction == 1.0:
                        result += f"• {name}: Price=${price:.2f}, Value={value:.2f}\n"
                    else:
                        result += f"• {name}: {fraction*100:.1f}% - Price=${price*fraction:.2f}, Value={value*fraction:.2f}\n"
                
                result += f"\nTotal Cost: ${total_cost:.2f}\n"
                result += f"Total Value: {total_value:.2f}\n"
                result += f"Remaining Budget: ${(budget - total_cost):.2f}"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)
            
            self.status_var.set(f"Optimization complete using {algorithm} knapsack")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid budget")

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetPlanner(root)
    root.mainloop() 
