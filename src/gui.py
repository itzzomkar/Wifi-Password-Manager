import tkinter as tk
from tkinter import messagebox
import os
from database import DatabaseManager

class WifiPasswordManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Wi-Fi Password Manager")
        self.root.geometry("400x300")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize database manager
        self.db_manager = DatabaseManager()
        
        self.show_login_screen()
    
    def show_login_screen(self):
        """Display the master password login screen"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create main frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Center frame
        center_frame = tk.Frame(main_frame, bg="#f0f0f0")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title
        title_label = tk.Label(
            center_frame, 
            text="🔒 Wi-Fi Password Manager", 
            font=("Arial", 18, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        title_label.pack(pady=(0, 20))
        
        # Description
        desc_label = tk.Label(
            center_frame, 
            text="Enter your master password to unlock the database", 
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#666666"
        )
        desc_label.pack(pady=(0, 20))
        
        # Password frame
        password_frame = tk.Frame(center_frame, bg="#f0f0f0")
        password_frame.pack(fill="x", pady=10)
        
        tk.Label(
            password_frame, 
            text="Master Password:", 
            font=("Arial", 11, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        ).pack(anchor="w", pady=(0, 5))
        
        # Password entry with show/hide functionality
        password_container = tk.Frame(password_frame, bg="#f0f0f0")
        password_container.pack(fill="x", pady=5)
        
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(
            password_container, 
            textvariable=self.password_var, 
            show="*", 
            font=("Arial", 12),
            bg="white",
            fg="#333333",
            relief="solid",
            bd=1,
            width=30
        )
        self.password_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Show/Hide button
        self.show_hide_btn = tk.Button(
            password_container, 
            text="Show", 
            width=8, 
            command=self.toggle_password_visibility,
            bg="#e0e0e0",
            fg="#333333",
            relief="raised",
            bd=1
        )
        self.show_hide_btn.pack(side="right")
        
        # Buttons frame
        buttons_frame = tk.Frame(center_frame, bg="#f0f0f0")
        buttons_frame.pack(fill="x", pady=20)
        
        # Login button
        login_btn = tk.Button(
            buttons_frame, 
            text="🔓 Unlock Database", 
            command=self.unlock_database,
            bg="#4a90e2",
            fg="white",
            relief="raised",
            bd=1,
            padx=20,
            pady=8,
            font=("Arial", 10, "bold")
        )
        login_btn.pack()
        
        # Bind Enter key to login
        self.password_entry.bind("<Return>", lambda event: self.unlock_database())
        
        # Focus on password entry
        self.password_entry.focus()
    
    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.password_entry.cget("show") == "*":
            self.password_entry.config(show="")
            self.show_hide_btn.config(text="Hide", bg="#d0d0d0")
        else:
            self.password_entry.config(show="*")
            self.show_hide_btn.config(text="Show", bg="#e0e0e0")
    
    def unlock_database(self):
        """Attempt to unlock the database with the provided password"""
        password = self.password_var.get()
        
        # Strip whitespace and check if empty
        password = password.strip()
        
        if not password:
            messagebox.showerror("Error", "Please enter a master password")
            return
        
        # Check if database exists
        if os.path.exists("wifi_data.enc"):
            # Try to unlock existing database
            if self.db_manager.unlock_database(password):
                messagebox.showinfo("Success", "Database unlocked successfully!")
                self.show_dashboard()
            else:
                messagebox.showerror("Error", "Invalid master password")
        else:
            # Initialize new database
            if self.db_manager.initialize_database(password):
                messagebox.showinfo("Success", "Database initialized successfully!")
                self.show_dashboard()
            else:
                messagebox.showerror("Error", "Failed to initialize database")
    
    def show_dashboard(self):
        """Display the main dashboard"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create main frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Center frame
        center_frame = tk.Frame(main_frame, bg="#f0f0f0")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Welcome message
        welcome_label = tk.Label(
            center_frame, 
            text="✅ Success!", 
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
            fg="#4a90e2"
        )
        welcome_label.pack(pady=10)
        
        info_label = tk.Label(
            center_frame, 
            text="The Wi-Fi Password Manager is ready for use.",
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#666666"
        )
        info_label.pack(pady=10)
        
        features_frame = tk.Frame(center_frame, bg="#f0f0f0")
        features_frame.pack(pady=20)
        
        features = [
            "🔒 Military-grade AES-256 encryption",
            "📱 Generate QR codes for easy sharing",
            "💾 All data stored locally",
            "🚫 No internet required"
        ]
        
        for feature in features:
            tk.Label(
                features_frame,
                text=feature,
                font=("Arial", 10),
                bg="#f0f0f0",
                fg="#333333"
            ).pack(pady=3, anchor="w")
        
        # Buttons
        buttons_frame = tk.Frame(center_frame, bg="#f0f0f0")
        buttons_frame.pack(pady=20)
        
        tk.Button(
            buttons_frame,
            text="🔒 Add Wi-Fi Network",
            command=lambda: messagebox.showinfo("Info", "Feature available in full version"),
            bg="#e0e0e0",
            fg="#333333",
            relief="raised",
            bd=1,
            padx=15,
            pady=5
        ).pack(side="left", padx=5)
        
        tk.Button(
            buttons_frame,
            text="🚪 Logout",
            command=self.show_login_screen,
            bg="#e0e0e0",
            fg="#333333",
            relief="raised",
            bd=1,
            padx=15,
            pady=5
        ).pack(side="left", padx=5)

def main():
    root = tk.Tk()
    app = WifiPasswordManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()