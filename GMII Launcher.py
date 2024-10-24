import json
import customtkinter as ctk
from tkinter import messagebox
import os

# File containing credentials
credentials_file = "credentials.json"

# Load credentials from JSON file
try:
    with open(credentials_file, "r") as f:
        credentials = json.load(f)
except FileNotFoundError:
    messagebox.showerror("Error", f"File not found: {credentials_file}")
    exit()

# Function to validate login
def validate_login():
    username = username_entry.get()
    password = password_entry.get()

    if username in credentials and credentials[username] == password:
        messagebox.showinfo("Login Successful", "Greetings!")
        os.startfile("D:\\Coding\\Python\\Gemini AI APP\\Gemini Mark II - College edition.py")
    else:
        messagebox.showerror("Login Error", "Invalid username or password. Please try again.")

# Initialize customtkinter settings
ctk.set_appearance_mode("dark")  # Modes: "dark" or "light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "dark-blue", or "green"

# Create the login window
root = ctk.CTk()
root.title("Login")

# Set window size to 500x300
root.geometry("600x500")

# Add padding to the window layout
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

# Create frame to center the elements
frame = ctk.CTkFrame(root, width=450, height=350, corner_radius=22, fg_color="black", border_color="white", border_width=5)
frame.grid(row=0, column=0, padx=20, pady=20)

# Username label and entry
username_label = ctk.CTkLabel(frame, text="Username:", font=("Arial", 14))
username_label.pack(pady=10)

username_entry = ctk.CTkEntry(frame, placeholder_text="Enter username", width=200)
username_entry.pack(pady=10)

# Password label and entry (use show="*" for password masking)
password_label = ctk.CTkLabel(frame, text="Password:", font=("Arial", 14))
password_label.pack(pady=10)

password_entry = ctk.CTkEntry(frame, placeholder_text="Enter password", show="*", width=200)
password_entry.pack(pady=10)

# Login and Cancel buttons
login_button = ctk.CTkButton(frame, text="Login", command=validate_login, width=100, corner_radius=32,
                             fg_color="purple", hover_color="light pink", border_color="indigo", 
                             border_width=2, text_color="white", font=("Calibri", 16, "bold"), 
                             text_color_disabled="white")
login_button.pack(pady=10)

cancel_button = ctk.CTkButton(frame, text="Cancel", command=root.quit, width=100, corner_radius=32,
                              fg_color="orange", hover_color="red", border_color="yellow",
                              border_width=2, text_color="white", font=("Calibri", 16, "bold"),
                              text_color_disabled="yellow")
cancel_button.pack(pady=10)

# Run the application
root.mainloop()
