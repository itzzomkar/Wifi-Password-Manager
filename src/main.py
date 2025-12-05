import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add src directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import DatabaseManager
from qrcode_generator import generate_wifi_qr
from utils import validate_ssid, validate_password, validate_security_type

class WifiPasswordManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Wi-Fi Password Manager")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Set window icon if available
        icon_path = os.path.join("assets", "app_icon.png")
        if os.path.exists(icon_path):
            try:
                self.root.iconphoto(False, tk.PhotoImage(file=icon_path))
            except:
                pass  # Ignore if icon loading fails
        
        # Initialize database manager
        self.db_manager = DatabaseManager()
        
        # Track current page
        self.current_page = None
        
        # Track theme
        self.dark_mode = False
        self.apply_theme()
        
        # Show login screen initially
        self.show_login_screen()
    
    def apply_theme(self):
        """Apply the current theme to the application"""
        if self.dark_mode:
            # Dark theme colors
            self.bg_color = "#2c2c2c"
            self.fg_color = "#ffffff"
            self.button_color = "#444444"
            self.entry_bg = "#3e3e3e"
            self.sidebar_color = "#1e1e1e"
            self.header_color = "#3a3a3a"
            self.select_bg = "#555555"
        else:
            # Light theme colors
            self.bg_color = "#f0f0f0"
            self.fg_color = "#000000"
            self.button_color = "#e0e0e0"
            self.entry_bg = "#ffffff"
            self.sidebar_color = "#e0e0e0"
            self.header_color = "#d0d0d0"
            self.select_bg = "#d0d0d0"
    
    def show_login_screen(self):
        """Display the master password login screen"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.current_page = "login"
        
        # Create main frame
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Center frame
        center_frame = tk.Frame(main_frame, bg=self.bg_color)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Header frame
        header_frame = tk.Frame(center_frame, bg=self.header_color, padx=30, pady=20)
        header_frame.pack(fill="x", pady=(0, 30))
        
        # Title
        title_label = tk.Label(
            header_frame, 
            text="🔒 Wi-Fi Password Manager", 
            font=("Arial", 24, "bold"),
            bg=self.header_color,
            fg=self.fg_color
        )
        title_label.pack()
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Securely store and manage your Wi-Fi credentials",
            font=("Arial", 12),
            bg=self.header_color,
            fg=self.fg_color
        )
        subtitle_label.pack(pady=(10, 0))
        
        # Login form frame
        form_frame = tk.Frame(center_frame, bg=self.bg_color)
        form_frame.pack(fill="x", padx=40, pady=20)
        
        # Description
        desc_label = tk.Label(
            form_frame, 
            text="Enter your master password to unlock the database", 
            font=("Arial", 12),
            bg=self.bg_color,
            fg=self.fg_color
        )
        desc_label.pack(pady=(0, 20))
        
        # Password frame
        password_frame = tk.Frame(form_frame, bg=self.bg_color)
        password_frame.pack(fill="x", pady=10)
        
        tk.Label(
            password_frame, 
            text="Master Password:", 
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(anchor="w", pady=(0, 5))
        
        # Password entry with show/hide functionality
        password_container = tk.Frame(password_frame, bg=self.bg_color)
        password_container.pack(fill="x", pady=5)
        
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(
            password_container, 
            textvariable=self.password_var, 
            show="*", 
            font=("Arial", 14),
            bg=self.entry_bg,
            fg=self.fg_color,
            relief="solid",
            bd=1
        )
        self.password_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Show/Hide button
        self.show_hide_btn = tk.Button(
            password_container, 
            text="Show", 
            width=10, 
            command=self.toggle_password_visibility,
            bg=self.button_color,
            fg=self.fg_color,
            relief="raised",
            bd=1
        )
        self.show_hide_btn.pack(side="right")
        
        # Buttons frame
        buttons_frame = tk.Frame(form_frame, bg=self.bg_color)
        buttons_frame.pack(fill="x", pady=20)
        
        # Login button
        login_btn = tk.Button(
            buttons_frame, 
            text="🔓 Unlock Database", 
            command=self.unlock_database,
            bg=self.button_color,
            fg=self.fg_color,
            relief="raised",
            bd=1,
            padx=15,
            pady=8,
            font=("Arial", 10, "bold")
        )
        login_btn.pack(side="left", padx=(0, 10))
        
        # Forgot password button
        forgot_btn = tk.Button(
            buttons_frame, 
            text="❓ Forgot Password", 
            command=self.show_forgot_password,
            bg=self.button_color,
            fg=self.fg_color,
            relief="raised",
            bd=1,
            padx=15,
            pady=8,
            font=("Arial", 10, "bold")
        )
        forgot_btn.pack(side="left", padx=(0, 10))
        
        # Theme toggle button
        theme_btn = tk.Button(
            buttons_frame, 
            text="🌓 Toggle Theme", 
            command=self.toggle_theme,
            bg=self.button_color,
            fg=self.fg_color,
            relief="raised",
            bd=1,
            padx=15,
            pady=8,
            font=("Arial", 10, "bold")
        )
        theme_btn.pack(side="left")
        
        # Bind Enter key to login
        self.password_entry.bind("<Return>", lambda event: self.unlock_database())
        
        # Footer
        footer_frame = tk.Frame(center_frame, bg=self.bg_color)
        footer_frame.pack(fill="x", pady=(30, 0))
        
        footer_label = tk.Label(
            footer_frame,
            text="All data is encrypted and stored locally on your device",
            font=("Arial", 9),
            bg=self.bg_color,
            fg=self.fg_color
        )
        footer_label.pack()
        
        # Focus on password entry
        self.password_entry.focus()
    
    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.password_entry.cget("show") == "*":
            self.password_entry.config(show="")
            self.show_hide_btn.config(text="Hide")
        else:
            self.password_entry.config(show="*")
            self.show_hide_btn.config(text="Show")
    
    def show_forgot_password(self):
        """Show forgot password dialog"""
        # Check if database exists
        if not os.path.exists("wifi_data.enc"):
            messagebox.showinfo("Info", "No database found. You can create a new one by entering a master password.")
            return
        
        # Confirmation dialog
        result = messagebox.askyesno(
            "Forgot Password", 
            "WARNING: Resetting your master password will DELETE ALL saved Wi-Fi networks!\n\n"
            "This action cannot be undone. Are you sure you want to proceed?"
        )
        
        if result:
            # Delete database files
            try:
                if os.path.exists("wifi_data.enc"):
                    os.remove("wifi_data.enc")
                if os.path.exists("master_key.hash"):
                    os.remove("master_key.hash")
                
                messagebox.showinfo(
                    "Reset Complete", 
                    "Master password has been reset. All saved Wi-Fi networks have been deleted.\n\n"
                    "You can now create a new master password."
                )
                
                # Refresh login screen
                self.show_login_screen()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to reset password: {str(e)}")
    
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
    
    def toggle_theme(self):
        """Toggle between dark and light mode"""
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        
        # Refresh current page to apply theme
        if self.current_page:
            if self.current_page == "login":
                self.show_login_screen()
            elif self.current_page == "dashboard":
                self.show_dashboard()
            elif self.current_page == "add":
                self.show_add_wifi()
            elif self.current_page == "view":
                self.show_view_wifi()
            elif self.current_page == "qr":
                self.show_generate_qr()
    
    def show_dashboard(self):
        """Display the main dashboard"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.current_page = "dashboard"
        
        # Create main frame
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(expand=True, fill="both")
        
        # Create header
        header_frame = tk.Frame(main_frame, bg=self.header_color, height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame, 
            text="📶 Wi-Fi Password Manager", 
            font=("Arial", 18, "bold"),
            bg=self.header_color,
            fg=self.fg_color
        )
        title_label.pack(side="left", padx=20, pady=15)
        
        # Theme toggle button
        theme_btn = tk.Button(
            header_frame, 
            text="🌓", 
            command=self.toggle_theme, 
            width=5,
            bg=self.button_color,
            fg=self.fg_color,
            relief="raised",
            bd=1
        )
        theme_btn.pack(side="right", padx=10, pady=10)
        
        # Logout button
        logout_btn = tk.Button(
            header_frame, 
            text="🚪 Logout", 
            command=self.show_login_screen, 
            width=10,
            bg=self.button_color,
            fg=self.fg_color,
            relief="raised",
            bd=1
        )
        logout_btn.pack(side="right", padx=5, pady=10)
        
        # Create content area with sidebar
        content_frame = tk.Frame(main_frame, bg=self.bg_color)
        content_frame.pack(expand=True, fill="both")
        
        # Create sidebar
        sidebar = tk.Frame(content_frame, bg=self.sidebar_color, width=220)
        sidebar.pack(side="left", fill="y", padx=(0, 10))
        sidebar.pack_propagate(False)
        
        # Sidebar title
        sidebar_title = tk.Label(
            sidebar, 
            text="Navigation", 
            font=("Arial", 14, "bold"),
            bg=self.sidebar_color,
            fg=self.fg_color,
            pady=20
        )
        sidebar_title.pack()
        
        # Navigation buttons with icons
        nav_buttons_frame = tk.Frame(sidebar, bg=self.sidebar_color)
        nav_buttons_frame.pack(fill="x", padx=10)
        
        tk.Button(
            nav_buttons_frame, 
            text="➕ Add Wi-Fi", 
            command=self.show_add_wifi,
            bg=self.button_color,
            fg=self.fg_color,
            relief="raised",
            bd=1,
            pady=8
        ).pack(fill="x", pady=5)
        
        tk.Button(
            nav_buttons_frame, 
            text="📋 View Wi-Fi", 
            command=self.show_view_wifi,
            bg=self.button_color,
            fg=self.fg_color,
            relief="raised",
            bd=1,
            pady=8
        ).pack(fill="x", pady=5)
        
        tk.Button(
            nav_buttons_frame, 
            text="📱 Generate QR", 
            command=self.show_generate_qr,
            bg=self.button_color,
            fg=self.fg_color,
            relief="raised",
            bd=1,
            pady=8
        ).pack(fill="x", pady=5)
        
        # Separator
        separator = tk.Frame(sidebar, height=2, bg="#cccccc")
        separator.pack(fill="x", pady=20)
        
        # Info section
        info_frame = tk.Frame(sidebar, bg=self.sidebar_color)
        info_frame.pack(fill="x", padx=10)
        
        info_label = tk.Label(
            info_frame,
            text="🔒 All data is encrypted\n💾 Stored locally\n🚫 No internet required",
            font=("Arial", 9),
            bg=self.sidebar_color,
            fg=self.fg_color,
            justify="left"
        )
        info_label.pack()
        
        # Main content area
        self.content_frame = tk.Frame(content_frame, bg=self.bg_color)
        self.content_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)
        
        # Welcome message
        welcome_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        welcome_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        welcome_label = tk.Label(
            welcome_frame, 
            text="Welcome to Wi-Fi Password Manager", 
            font=("Arial", 20, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        welcome_label.pack(pady=10)
        
        instruction_label = tk.Label(
            welcome_frame, 
            text="Use the sidebar to navigate between different functions",
            font=("Arial", 12),
            bg=self.bg_color,
            fg=self.fg_color
        )
        instruction_label.pack()
        
        # Feature highlights
        features_frame = tk.Frame(welcome_frame, bg=self.bg_color)
        features_frame.pack(pady=30)
        
        features = [
            ("🔒", "Military-grade AES-256 encryption"),
            ("📱", "Generate QR codes for easy sharing"),
            ("🌓", "Light/Dark theme support"),
            ("💻", "Works completely offline")
        ]
        
        for i, (emoji, text) in enumerate(features):
            feature_frame = tk.Frame(features_frame, bg=self.bg_color)
            feature_frame.pack(fill="x", pady=5)
            
            tk.Label(
                feature_frame,
                text=emoji,
                font=("Arial", 14),
                bg=self.bg_color,
                fg=self.fg_color
            ).pack(side="left", padx=(0, 10))
            
            tk.Label(
                feature_frame,
                text=text,
                font=("Arial", 11),
                bg=self.bg_color,
                fg=self.fg_color
            ).pack(side="left")
    
    def show_add_wifi(self):
        """Display the add Wi-Fi form"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        self.current_page = "add"
        
        # Scrollable canvas
        canvas = tk.Canvas(self.content_frame, bg=self.bg_color, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Title
        title_label = tk.Label(
            scrollable_frame, 
            text="➕ Add New Wi-Fi Network", 
            font=("Arial", 18, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        title_label.pack(pady=(0, 20))
        
        # Form container
        form_container = tk.Frame(scrollable_frame, bg=self.bg_color)
        form_container.pack(fill="x", padx=20)
        
        # Form frame
        form_frame = tk.Frame(form_container, bg=self.bg_color)
        form_frame.pack(fill="x", pady=10)
        
        # SSID
        ssid_frame = tk.Frame(form_frame, bg=self.bg_color)
        ssid_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(
            ssid_frame, 
            text="📡 Network Name (SSID):", 
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(anchor="w", pady=(0, 5))
        
        self.ssid_var = tk.StringVar()
        ssid_entry = tk.Entry(
            ssid_frame, 
            textvariable=self.ssid_var,
            font=("Arial", 12),
            bg=self.entry_bg,
            fg=self.fg_color,
            relief="solid",
            bd=1
        )
        ssid_entry.pack(fill="x", pady=(0, 5))
        
        # Password
        password_frame = tk.Frame(form_frame, bg=self.bg_color)
        password_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(
            password_frame, 
            text="🔑 Password:", 
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(anchor="w", pady=(0, 5))
        
        password_container = tk.Frame(password_frame, bg=self.bg_color)
        password_container.pack(fill="x")
        
        self.wifi_password_var = tk.StringVar()
        self.wifi_password_entry = tk.Entry(
            password_container, 
            textvariable=self.wifi_password_var,
            show="*", 
            font=("Arial", 12),
            bg=self.entry_bg,
            fg=self.fg_color,
            relief="solid",
            bd=1
        )
        self.wifi_password_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.wifi_show_hide_btn = tk.Button(
            password_container, 
            text="Show", 
            width=10, 
            command=self.toggle_wifi_password_visibility,
            bg=self.button_color,
            fg=self.fg_color,
            relief="raised",
            bd=1
        )
        self.wifi_show_hide_btn.pack(side="right")
        
        # Security Type
        security_frame = tk.Frame(form_frame, bg=self.bg_color)
        security_frame.pack(fill="x", pady=(0, 30))
        
        tk.Label(
            security_frame, 
            text="🛡️ Security Type:", 
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(anchor="w", pady=(0, 5))
        
        self.security_var = tk.StringVar(value="WPA")
        security_combo = ttk.Combobox(
            security_frame, 
            textvariable=self.security_var, 
            values=["WPA", "WPA2", "WEP", "NOPASS"],
            state="readonly",
            font=("Arial", 11)
        )
        security_combo.pack(fill="x", pady=(0, 5))
        
        # Info text
        info_label = tk.Label(
            security_frame,
            text="Select the security protocol used by your Wi-Fi network",
            font=("Arial", 9),
            bg=self.bg_color,
            fg=self.fg_color
        )
        info_label.pack(anchor="w")
        
        # Buttons
        buttons_frame = tk.Frame(form_frame, bg=self.bg_color)
        buttons_frame.pack(fill="x", pady=10)
        
        save_btn = tk.Button(
            buttons_frame, 
            text="💾 Save Network", 
            command=self.save_wifi_credential,
            bg=self.button_color,
            fg=self.fg_color,
            relief="raised",
            bd=1,
            padx=15,
            pady=8,
            font=("Arial", 10, "bold")
        )
        save_btn.pack(side="left", padx=(0, 15))
        
        clear_btn = tk.Button(
            buttons_frame, 
            text="🧹 Clear Form", 
            command=self.clear_wifi_form,
            bg=self.button_color,
            fg=self.fg_color,
            relief="raised",
            bd=1,
            padx=15,
            pady=8,
            font=("Arial", 10, "bold")
        )
        clear_btn.pack(side="left")
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def toggle_wifi_password_visibility(self):
        """Toggle Wi-Fi password visibility"""
        if self.wifi_password_entry.cget("show") == "*":
            self.wifi_password_entry.config(show="")
            self.wifi_show_hide_btn.config(text="Hide")
        else:
            self.wifi_password_entry.config(show="*")
            self.wifi_show_hide_btn.config(text="Show")
    
    def save_wifi_credential(self):
        """Save the Wi-Fi credential to the database"""
        ssid = self.ssid_var.get().strip()
        password = self.wifi_password_var.get()
        security = self.security_var.get()
        
        # Validate inputs
        if not validate_ssid(ssid):
            messagebox.showerror("Error", "Please enter a valid SSID (1-32 characters)")
            return
        
        if security.upper() != "NOPASS" and not password:
            messagebox.showerror("Error", "Please enter a password")
            return
        
        if not validate_security_type(security):
            messagebox.showerror("Error", "Please select a valid security type")
            return
        
        if security.upper() != "NOPASS" and not validate_password(password, security):
            if security.upper() in ["WPA", "WPA2"]:
                messagebox.showerror("Error", "WPA/WPA2 passwords must be 8-63 characters")
            elif security.upper() == "WEP":
                messagebox.showerror("Error", "WEP password must be 5/13 ASCII characters or 10/26 hex characters")
            else:
                messagebox.showerror("Error", "Please enter a valid password")
            return
        
        # Save to database
        if self.db_manager.add_wifi(ssid, password, security):
            messagebox.showinfo("Success", f"Wi-Fi network '{ssid}' saved successfully!")
            self.clear_wifi_form()
        else:
            messagebox.showerror("Error", "Failed to save Wi-Fi network")
    
    def clear_wifi_form(self):
        """Clear the Wi-Fi form"""
        self.ssid_var.set("")
        self.wifi_password_var.set("")
        self.security_var.set("WPA")
        
        # Reset password visibility
        self.wifi_password_entry.config(show="*")
        self.wifi_show_hide_btn.config(text="Show")
    
    def show_view_wifi(self):
        """Display the view Wi-Fi credentials page"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        self.current_page = "view"
        
        # Title
        title_label = tk.Label(
            self.content_frame, 
            text="📋 Saved Wi-Fi Networks", 
            font=("Arial", 18, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        title_label.pack(pady=(0, 20))
        
        # Controls frame
        controls_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        controls_frame.pack(fill="x", pady=(0, 15))
        
        refresh_btn = tk.Button(
            controls_frame, 
            text="🔄 Refresh", 
            command=self.load_wifi_credentials,
            bg=self.button_color,
            fg=self.fg_color,
            relief="raised",
            bd=1,
            padx=15,
            pady=8,
            font=("Arial", 10, "bold")
        )
        refresh_btn.pack(side="left", padx=(0, 10))
        
        delete_btn = tk.Button(
            controls_frame, 
            text="🗑️ Delete Selected", 
            command=self.delete_selected_wifi,
            bg=self.button_color,
            fg=self.fg_color,
            relief="raised",
            bd=1,
            padx=15,
            pady=8,
            font=("Arial", 10, "bold")
        )
        delete_btn.pack(side="left", padx=(0, 10))
        
        copy_btn = tk.Button(
            controls_frame, 
            text="📋 Copy Password", 
            command=self.copy_selected_password,
            bg=self.button_color,
            fg=self.fg_color,
            relief="raised",
            bd=1,
            padx=15,
            pady=8,
            font=("Arial", 10, "bold")
        )
        copy_btn.pack(side="left")
        
        # Create treeview for displaying Wi-Fi networks with scrollbar
        tree_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        tree_frame.pack(fill="both", expand=True)
        
        # Define columns
        columns = ("SSID", "Security", "Password")
        
        # Create treeview
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        # Define headings
        self.tree.heading("SSID", text="📡 Network Name")
        self.tree.heading("Security", text="🛡️ Security")
        self.tree.heading("Password", text="🔑 Password")
        
        # Define column widths
        self.tree.column("SSID", width=250)
        self.tree.column("Security", width=120)
        self.tree.column("Password", width=250)
        
        # Add scrollbars
        v_scrollbar = tk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = tk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.tree.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        
        # Style the treeview
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), background=self.entry_bg, fieldbackground=self.entry_bg, foreground=self.fg_color)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        
        # Load Wi-Fi credentials
        self.load_wifi_credentials()
    
    def load_wifi_credentials(self):
        """Load and display Wi-Fi credentials in the treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load credentials from database
        credentials = self.db_manager.get_all_wifi()
        
        # Add credentials to treeview
        for cred in credentials:
            # Hide password characters for display
            display_password = "*" * len(cred["password"]) if cred["password"] else ""
            self.tree.insert("", "end", values=(cred["ssid"], cred["security"], display_password))
    
    def delete_selected_wifi(self):
        """Delete the selected Wi-Fi network"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select a network to delete")
            return
        
        # Get the SSID of the selected item
        item = self.tree.item(selected_items[0])
        ssid = item["values"][0]
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{ssid}'?"):
            if self.db_manager.delete_wifi(ssid):
                messagebox.showinfo("Success", f"Network '{ssid}' deleted successfully!")
                self.load_wifi_credentials()
            else:
                messagebox.showerror("Error", "Failed to delete network")
    
    def copy_selected_password(self):
        """Copy the password of the selected Wi-Fi network"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select a network to copy password")
            return
        
        # Get the SSID of the selected item
        item = self.tree.item(selected_items[0])
        ssid = item["values"][0]
        
        # Find the actual password from the database
        credentials = self.db_manager.get_all_wifi()
        password = ""
        for cred in credentials:
            if cred["ssid"] == ssid:
                password = cred["password"]
                break
        
        if password:
            # Copy to clipboard
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            self.root.update()
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        else:
            messagebox.showerror("Error", "Could not find password")
    
    def show_generate_qr(self):
        """Display the generate QR code page"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        self.current_page = "qr"
        
        # Title
        title_label = tk.Label(
            self.content_frame, 
            text="📱 Generate Wi-Fi QR Code", 
            font=("Arial", 18, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        title_label.pack(pady=(0, 20))
        
        # Instruction
        instruction_label = tk.Label(
            self.content_frame, 
            text="Select a network to generate a QR code for easy sharing",
            font=("Arial", 11),
            bg=self.bg_color,
            fg=self.fg_color
        )
        instruction_label.pack(pady=(0, 20))
        
        # Controls frame
        controls_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        controls_frame.pack(fill="x", pady=(0, 15))
        
        refresh_btn = tk.Button(
            controls_frame, 
            text="🔄 Refresh", 
            command=self.load_wifi_for_qr,
            bg=self.button_color,
            fg=self.fg_color,
            relief="raised",
            bd=1,
            padx=15,
            pady=8,
            font=("Arial", 10, "bold")
        )
        refresh_btn.pack(side="left", padx=(0, 10))
        
        generate_btn = tk.Button(
            controls_frame, 
            text="📱 Generate QR Code", 
            command=self.generate_selected_qr,
            bg=self.button_color,
            fg=self.fg_color,
            relief="raised",
            bd=1,
            padx=15,
            pady=8,
            font=("Arial", 10, "bold")
        )
        generate_btn.pack(side="left")
        
        # Create treeview for selecting network
        tree_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        tree_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Define columns
        columns = ("SSID", "Security")
        
        # Create treeview
        self.qr_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
        
        # Define headings
        self.qr_tree.heading("SSID", text="📡 Network Name")
        self.qr_tree.heading("Security", text="🛡️ Security")
        
        # Define column widths
        self.qr_tree.column("SSID", width=300)
        self.qr_tree.column("Security", width=150)
        
        # Add scrollbar
        qr_scrollbar = tk.Scrollbar(tree_frame, orient="vertical", command=self.qr_tree.yview)
        self.qr_tree.configure(yscrollcommand=qr_scrollbar.set)
        
        # Pack treeview and scrollbar
        self.qr_tree.pack(side="left", fill="both", expand=True)
        qr_scrollbar.pack(side="right", fill="y")
        
        # Style the treeview
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), background=self.entry_bg, fieldbackground=self.entry_bg, foreground=self.fg_color)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        
        # QR code display area
        self.qr_display_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        self.qr_display_frame.pack(fill="both", expand=True)
        
        # Load Wi-Fi credentials
        self.load_wifi_for_qr()
    
    def load_wifi_for_qr(self):
        """Load Wi-Fi credentials for QR code generation"""
        # Clear existing items
        for item in self.qr_tree.get_children():
            self.qr_tree.delete(item)
        
        # Load credentials from database
        credentials = self.db_manager.get_all_wifi()
        
        # Add credentials to treeview
        for cred in credentials:
            self.qr_tree.insert("", "end", values=(cred["ssid"], cred["security"]))
    
    def generate_selected_qr(self):
        """Generate QR code for the selected Wi-Fi network"""
        selected_items = self.qr_tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select a network to generate QR code")
            return
        
        # Get the SSID of the selected item
        item = self.qr_tree.item(selected_items[0])
        ssid = item["values"][0]
        security = item["values"][1]
        
        # Find the actual password from the database
        credentials = self.db_manager.get_all_wifi()
        password = ""
        for cred in credentials:
            if cred["ssid"] == ssid:
                password = cred["password"]
                break
        
        try:
            # Generate QR code
            qr_path = generate_wifi_qr(ssid, password, security)
            
            # Display QR code
            self.display_qr_code(qr_path, ssid)
            
            messagebox.showinfo("Success", f"QR code generated successfully!\nSaved to: {qr_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code: {str(e)}")
    
    def display_qr_code(self, qr_path, ssid):
        """Display the generated QR code"""
        # Clear previous QR display
        for widget in self.qr_display_frame.winfo_children():
            widget.destroy()
        
        try:
            # Header
            header_label = tk.Label(
                self.qr_display_frame,
                text=f"QR Code for '{ssid}'",
                font=("Arial", 14, "bold"),
                bg=self.bg_color,
                fg=self.fg_color
            )
            header_label.pack(pady=(0, 10))
            
            # Load and display QR code
            qr_image = tk.PhotoImage(file=qr_path)
            
            # Resize if too large
            max_size = 300
            if qr_image.width() > max_size or qr_image.height() > max_size:
                # Calculate resize factor
                factor = min(max_size / qr_image.width(), max_size / qr_image.height())
                new_width = int(qr_image.width() * factor)
                new_height = int(qr_image.height() * factor)
                qr_image = qr_image.subsample(int(qr_image.width() / new_width), int(qr_image.height() / new_height))
            
            # Display image
            image_label = tk.Label(self.qr_display_frame, image=qr_image, bg=self.bg_color)
            image_label.image = qr_image  # Keep a reference
            image_label.pack(pady=10)
            
            # Display file path
            path_label = tk.Label(
                self.qr_display_frame, 
                text=f"Saved to: {qr_path}", 
                font=("Arial", 9),
                bg=self.bg_color,
                fg=self.fg_color,
                wraplength=500
            )
            path_label.pack(pady=(10, 0))
            
            # Instructions
            instructions_label = tk.Label(
                self.qr_display_frame,
                text="Scan this QR code with your mobile device to connect to the Wi-Fi network",
                font=("Arial", 10),
                bg=self.bg_color,
                fg=self.fg_color
            )
            instructions_label.pack(pady=(10, 0))
            
        except Exception as e:
            error_label = tk.Label(
                self.qr_display_frame, 
                text=f"Failed to display QR code: {str(e)}",
                font=("Arial", 10),
                bg=self.bg_color,
                fg="red"
            )
            error_label.pack()

def main():
    """Main entry point for the Wi-Fi Password Manager application"""
    # Create root window
    root = tk.Tk()
    
    # Create and run the GUI
    app = WifiPasswordManagerGUI(root)
    
    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()