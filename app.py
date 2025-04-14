import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Password Generator")
        self.root.geometry("500x450")
        self.root.resizable(False, False)
        
        # Configure style
        self.style = ttk.Style()
        self.configure_styles()
        
        self.setup_ui()
    
    def configure_styles(self):
        """Configure custom styles for widgets"""
        self.style.theme_use('clam')
        
        # Colors
        self.bg_color = "#f0f0f0"
        self.primary_color = "#4a6fa5"
        self.secondary_color = "#166088"
        self.accent_color = "#4fc3f7"
        self.text_color = "#333333"
        
        # Configure styles
        self.style.configure('.', background=self.bg_color, foreground=self.text_color)
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', background=self.bg_color, font=('Segoe UI', 10))
        self.style.configure('TButton', font=('Segoe UI', 10, 'bold'), padding=6)
        self.style.configure('Title.TLabel', font=('Segoe UI', 18, 'bold'), foreground=self.primary_color)
        self.style.configure('Password.TEntry', fieldbackground='white', font=('Consolas', 12))
        self.style.configure('Generate.TButton', background=self.primary_color, foreground='white')
        self.style.configure('Copy.TButton', background=self.secondary_color, foreground='white')
        
        # Slider style
        self.style.configure('Horizontal.TScale', troughcolor='#e0e0e0')
        
        # Option menu style
        self.style.map('TMenubutton', background=[('active', self.accent_color)])
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(main_frame, text="Password Generator", style='Title.TLabel').grid(
            row=0, column=0, columnspan=3, pady=(0, 15))
        
        # Length control
        ttk.Label(main_frame, text="Password Length:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.length_var = tk.IntVar(value=12)
        self.length_slider = ttk.Scale(
            main_frame, from_=8, to=128, variable=self.length_var, 
            command=self.update_length_label, style='Horizontal.TScale')
        self.length_slider.grid(row=1, column=1, sticky=tk.EW, pady=5)
        self.length_label = ttk.Label(main_frame, text="12", width=3)
        self.length_label.grid(row=1, column=2, padx=5)
        
        # Character types
        ttk.Label(main_frame, text="Character Types:").grid(row=2, column=0, sticky=tk.W, pady=5)
        
        char_frame = ttk.Frame(main_frame)
        char_frame.grid(row=2, column=1, columnspan=2, sticky=tk.W)
        
        self.lower_var = tk.BooleanVar(value=True)
        self.upper_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(char_frame, text="Lowercase (a-z)", variable=self.lower_var).grid(row=0, column=0, sticky=tk.W)
        ttk.Checkbutton(char_frame, text="Uppercase (A-Z)", variable=self.upper_var).grid(row=1, column=0, sticky=tk.W)
        ttk.Checkbutton(char_frame, text="Digits (0-9)", variable=self.digits_var).grid(row=2, column=0, sticky=tk.W)
        ttk.Checkbutton(char_frame, text="Symbols (!@#...)", variable=self.symbols_var).grid(row=3, column=0, sticky=tk.W)
        
        # Exclude characters
        ttk.Label(main_frame, text="Exclude Characters:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.exclude_var = tk.StringVar()
        exclude_entry = ttk.Entry(main_frame, textvariable=self.exclude_var, width=30)
        exclude_entry.grid(row=3, column=1, columnspan=2, sticky=tk.W)
        
        # Password strength
        ttk.Label(main_frame, text="Password Strength:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.strength_var = tk.StringVar(value="Medium")
        strength_options = ["Low", "Medium", "High", "Very High"]
        strength_menu = ttk.OptionMenu(
            main_frame, self.strength_var, "Medium", *strength_options)
        strength_menu.grid(row=4, column=1, sticky=tk.W)
        
        # Generate button
        generate_btn = ttk.Button(
            main_frame, text="Generate Password", command=self.generate_password,
            style='Generate.TButton')
        generate_btn.grid(row=5, column=0, columnspan=3, pady=15)
        
        # Generated password
        ttk.Label(main_frame, text="Generated Password:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(
            main_frame, textvariable=self.password_var, state='readonly', 
            style='Password.TEntry', width=30)
        password_entry.grid(row=6, column=1, columnspan=2)
        
        # Copy button
        copy_btn = ttk.Button(
            main_frame, text="Copy to Clipboard", command=self.copy_to_clipboard,
            style='Copy.TButton')
        copy_btn.grid(row=7, column=0, columnspan=3, pady=10)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
    
    def update_length_label(self, value):
        self.length_label.config(text=str(int(float(value))))
    
    def get_character_set(self):
        char_set = ""
        
        if self.lower_var.get():
            char_set += string.ascii_lowercase
        if self.upper_var.get():
            char_set += string.ascii_uppercase
        if self.digits_var.get():
            char_set += string.digits
        if self.symbols_var.get():
            char_set += string.punctuation
            
        # Remove excluded characters
        exclude_chars = self.exclude_var.get()
        if exclude_chars:
            char_set = ''.join([c for c in char_set if c not in exclude_chars])
        
        return char_set
    
    def validate_character_set(self, char_set):
        if not char_set:
            messagebox.showerror("Error", "No character types selected!")
            return False
        
        min_length = 8
        strength = self.strength_var.get()
        
        if strength == "Low":
            min_length = 8
        elif strength == "Medium":
            min_length = 12
        elif strength == "High":
            min_length = 16
        elif strength == "Very High":
            min_length = 20
            
        if self.length_var.get() < min_length:
            messagebox.showwarning("Warning", 
                                 f"For {strength} strength, password length should be at least {min_length} characters.")
            return False
            
        return True
    
    def generate_password(self):
        char_set = self.get_character_set()
        
        if not self.validate_character_set(char_set):
            return
            
        length = self.length_var.get()
        password = []
        
        # Ensure at least one character from each selected set
        if self.lower_var.get():
            password.append(random.choice(string.ascii_lowercase))
        if self.upper_var.get():
            password.append(random.choice(string.ascii_uppercase))
        if self.digits_var.get():
            password.append(random.choice(string.digits))
        if self.symbols_var.get():
            password.append(random.choice(string.punctuation))
        
        # Fill the rest with random characters
        remaining_length = length - len(password)
        for _ in range(remaining_length):
            password.append(random.choice(char_set))
        
        # Shuffle to avoid predictable patterns
        random.shuffle(password)
        
        self.password_var.set(''.join(password))
    
    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Success", "Password copied to clipboard!")
        else:
            messagebox.showerror("Error", "No password generated yet!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()