import os
import webbrowser
import customtkinter as ctk
from tkinter import messagebox

# Links to the resources
links = {
    "21pyb102j": "https://drive.google.com/drive/folders/1WPvAVR2vR0Iw0N-uWUxxL5dkg9-HzF4v",  # Physics
    "21css101j": "https://drive.google.com/drive/folders/1iGwJtKWz5Arahcul7onuHva8SizQ1E5G",  # Programming for Problem Solving
    "21gnh101j": "https://drive.google.com/drive/folders/1hktPcj_vDKY7Y3TqTvgrxLGNsL4uIiPc",  # Philosophy of Engineering
    "21mab101t": "https://drive.google.com/drive/folders/1D7iDXLMg4gmBApghenfDueqb2Od0jQa9",  # Mathematics
    "21leh101t": "https://drive.google.com/drive/folders/1f5JjZjy3I1rWKzl5MrVzerHUqCLg0y_k",  # English
    "21cyb101j": "https://drive.google.com/drive/folders/1lrtBwvJ3HVZPi_DH3i04uKxBMcCFLekw",  # Chemistry
    "21btb102t": "https://drive.google.com/drive/folders/1N9l92axthPtu2cnt7OZ3o7WOhf3ZyRSj",  # Biology
    "21pyq101t": "https://drive.google.com/drive/folders/1PfuyJyICqTEuq4BPvN6Y47g9-U_5Mdtr",  # All PYQs
}

# Function to search and open exam papers or notes
def search_exam_papers():
    """Search for exam papers by course code."""
    query = entry.get().lower()
    if query in links:
        webbrowser.open(links[query])
    else:
        messagebox.showinfo("Not Found", "No matching exam papers found.")

# Function to list all exam papers and notes
def list_exam_papers():
    """Display the list of papers and notes in a text widget."""
    paper_list = (
        "1. Physics: 21PYB102J\n"
        "2. Programming for Problem Solving: 21CSS101J\n"
        "3. Philosophy of Engineering: 21GNH101J\n"
        "4. Mathematics: 21MAB101T\n"
        "5. English: 21LEH101T\n"
        "6. Chemistry: 21CYB101J\n"
        "7. Biology: 21BTB102T\n"
        "8. All PYQs: 21PYQ101T\n"
    )
    text_widget.delete(1.0, ctk.END)  # Clear existing text
    text_widget.insert(ctk.END, paper_list)  # Insert the list of papers

# CustomTkinter setup
ctk.set_appearance_mode("dark")  # Modes: "light" or "dark"
ctk.set_default_color_theme("blue")  # Themes: "blue", "dark-blue", or "green"

# Create the main window
root = ctk.CTk()
root.geometry("500x500")
root.title("Past Papers and Notes Organizer")

# Create a frame for the output window
frame = ctk.CTkFrame(root, width=450, height=250, corner_radius=22, fg_color="black", border_color="white", border_width=5)
frame.pack(padx=20, pady=20)  # Use pack instead of grid for layout consistency

# Text widget to display exam papers within the frame
text_widget = ctk.CTkTextbox(frame, height=150, width=400, border_width=2, border_color="grey")  # Adjusted height and width for better display
text_widget.pack(padx=10, pady=10)

# Entry widget for course code input
entry = ctk.CTkEntry(root, width=300, border_color="cyan", border_width=2)
entry.pack(pady=5)

# Search button
search_button = ctk.CTkButton(root, text="Search", command=search_exam_papers, hover_color="green", border_color="grey", border_width=1, font=("calibri", 20, "bold"))
search_button.pack(pady=5)

# List papers button
list_button = ctk.CTkButton(root, text="List Papers", command=list_exam_papers, hover_color="cyan", border_color="grey", border_width=1, font=("calibri", 16, "bold"))
list_button.pack(pady=5)

# Exit button
exit_button = ctk.CTkButton(root, text="Exit", command=root.quit, hover_color="red", border_color="grey", border_width=1, font=("calibri", 20, "bold"))
exit_button.pack(pady=5)

# Run the main event loop
root.mainloop()
