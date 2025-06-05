import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Tuple
import random

class BudgetPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Planner - Knapsack Algorithms")
        self.root.geometry("900x700")
        
        # Items list to store (name, price, value) tuples
        self.items: List[Tuple[str, float, float]] = []
        
        # Algorithm selection
        self.algorithm_var = tk.StringVar(value="0/1")
        
        # Create widgets
        self.create_widgets()
        
    def create_widgets(self):
        # Input Frame
        input_frame = ttk.LabelFrame(self.root, text="Add Items", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Item name input
        ttk.Label(input_frame, text="Item Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.name_var).grid(row=0, column=1, padx=5, pady=5)
        
        # Price input
        ttk.Label(input_frame, text="Price:").grid(row=0, column=2, padx=5, pady=5)
        self.price_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.price_var).grid(row=0, column=3, padx=5, pady=5)
        
        # Value input
        ttk.Label(input_frame, text="Value (Importance):").grid(row=0, column=4, padx=5, pady=5)
        self.value_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.value_var).grid(row=0, column=5, padx=5, pady=5)
        
        # Add button
        ttk.Button(input_frame, text="Add Item", command=self.add_item).grid(row=0, column=6, padx=5, pady=5)
        
        # Algorithm selection frame
        algo_frame = ttk.LabelFrame(self.root, text="Algorithm Selection", padding=10)
        algo_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Radiobutton(algo_frame, text="0/1 Knapsack (Items cannot be divided)", 
                       variable=self.algorithm_var, value="0/1").pack(side="left", padx=10)
        
        ttk.Radiobutton(algo_frame, text="Fractional Knapsack (Items can be divided)", 
                       variable=self.algorithm_var, value="fractional").pack(side="left", padx=10)
        
        # Budget input
        budget_frame = ttk.LabelFrame(self.root, text="Budget", padding=10)
        budget_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(budget_frame, text="Total Budget:").pack(side="left", padx=5)
        self.budget_var = tk.StringVar()
        ttk.Entry(budget_frame, textvariable=self.budget_var).pack(side="left", padx=5)
        
        # Optimize button
        self.optimize_btn = ttk.Button(budget_frame, text="Optimize", command=self.optimize)
        self.optimize_btn.pack(side="left", padx=5)
        
        # Clear all button
        ttk.Button(budget_frame, text="Clear All", command=self.clear_all).pack(side="left", padx=5)
        
        # Items list display
        list_frame = ttk.LabelFrame(self.root, text="Items List", padding=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Create Treeview with scrollbar
        tree_frame = ttk.Frame(list_frame)
        tree_frame.pack(fill="both", expand=True)
        
        self.tree = ttk.Treeview(tree_frame, columns=("Name", "Price", "Value", "Value/Price"), show="headings")
        self.tree.heading("Name", text="Item Name")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Value", text="Value")
        self.tree.heading("Value/Price", text="Value/Price")
        
        # Configure column widths
        self.tree.column("Name", width=200)
        self.tree.column("Price", width=100)
        self.tree.column("Value", width=100)
        self.tree.column("Value/Price", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind double-click event
        self.tree.bind("<Double-1>", self.on_item_double_click)
        
        # Results display
        result_frame = ttk.LabelFrame(self.root, text="Results", padding=10)
        result_frame.pack(fill="x", padx=10, pady=5)
        
        self.result_text = tk.Text(result_frame, height=8, wrap=tk.WORD)
        self.result_text.pack(fill="x")
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief="sunken", anchor="w")
        status_bar.pack(fill="x", padx=10, pady=5)
        
    def add_item(self):
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