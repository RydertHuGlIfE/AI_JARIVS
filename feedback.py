import sqlite3
import customtkinter as ctk
from tkinter import messagebox, simpledialog

# Connect to SQLite database
conn = sqlite3.connect('feedback_form.db')
cursor = conn.cursor()

# Create a table to store feedback if it doesn't already exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    teacher TEXT NOT NULL,
    code TEXT NOT NULL,
    feedback TEXT NOT NULL
)
''')

# Functions
def submit_feedback():
    sub = subject_entry.get()
    teacher = teacher_entry.get()
    code = code_entry.get()
    feedback = feedback_text.get("1.0", ctk.END).strip()

    if sub and teacher and code and feedback:
        # Insert feedback into the database
        cursor.execute('''
        INSERT INTO feedback (subject, teacher, code, feedback)
        VALUES (?, ?, ?, ?)
        ''', (sub, teacher, code, feedback))

        conn.commit()  # Save the changes
        messagebox.showinfo("Success", "Your feedback has been submitted successfully.")
        clear_fields()
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields.")

def show_subjects_and_codes():
    cursor.execute('SELECT DISTINCT subject, teacher, code FROM feedback')
    subjects_and_teachers = cursor.fetchall()

    if not subjects_and_teachers:
        messagebox.showinfo("Info", "No subjects found in the database.")
    else:
        subjects_list = "\n".join(f"Subject: {subject}, Teacher: {teacher}, Code: {code}" 
                                   for subject, teacher, code in subjects_and_teachers)
        messagebox.showinfo("Subjects and Codes", subjects_list)

def filter_responses():
    subject_filter = simpledialog.askstring("Input", "Enter subject name:")
    code_filter = simpledialog.askstring("Input", "Enter subject code:")

    cursor.execute('''
    SELECT subject, code, feedback FROM feedback
    WHERE subject = ? AND code = ?
    ''', (subject_filter, code_filter))
    
    filtered_responses = cursor.fetchall()

    if not filtered_responses:
        messagebox.showinfo("Info", "No feedback found for the given subject and code.")
    else:
        responses_list = "\n".join(f"Subject: {response[0]}, Code: {response[1]}, Feedback: {response[2]}" 
                                   for response in filtered_responses)
        messagebox.showinfo("Filtered Feedback", responses_list)

def clear_fields():
    subject_entry.delete(0, ctk.END)
    teacher_entry.delete(0, ctk.END)
    code_entry.delete(0, ctk.END)
    feedback_text.delete("1.0", ctk.END)

# CustomTkinter setup
ctk.set_appearance_mode("dark")  # Modes: "light" or "dark"
ctk.set_default_color_theme("blue")  # Themes: "blue", "dark-blue", or "green"

# Create the main window
root = ctk.CTk()
root.geometry("500x500")
root.title("Feedback Form")

# Create a frame for better appearance
frame = ctk.CTkFrame(root, corner_radius=15, fg_color="black", border_color="white", border_width=4)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Create input fields with customtkinter widgets
subject_label = ctk.CTkLabel(frame, text="Subject Name:")
subject_label.grid(row=0, column=0, padx=10, pady=(20, 10))  # Add top padding for space
subject_entry = ctk.CTkEntry(frame, width=200, border_color="#03638c", border_width=3)
subject_entry.grid(row=0, column=1, padx=10, pady=10)

teacher_label = ctk.CTkLabel(frame, text="Teacher Name:")
teacher_label.grid(row=1, column=0, padx=10, pady=10)
teacher_entry = ctk.CTkEntry(frame, width=200, border_color="#03638c", border_width=3)
teacher_entry.grid(row=1, column=1, padx=10, pady=10)

code_label = ctk.CTkLabel(frame, text="Subject Code:")
code_label.grid(row=2, column=0, padx=10, pady=10)
code_entry = ctk.CTkEntry(frame, width=200, border_color="#03638c", border_width=3)
code_entry.grid(row=2, column=1, padx=10, pady=10)

feedback_label = ctk.CTkLabel(frame, text="Feedback:")
feedback_label.grid(row=3, column=0, padx=10, pady=10)
feedback_text = ctk.CTkTextbox(frame, width=250, height=90, border_color="white", border_width=2)
feedback_text.grid(row=3, column=1, padx=10, pady=10)

# Create buttons with customtkinter widgets and center them
submit_button = ctk.CTkButton(frame, text="Submit Feedback", command=submit_feedback, fg_color="indigo", hover_color="green")
submit_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

view_subjects_button = ctk.CTkButton(frame, text="View Subject List", command=show_subjects_and_codes, fg_color="indigo", hover_color="magenta")
view_subjects_button.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

view_responses_button = ctk.CTkButton(frame, text="Show Previous Responses", command=filter_responses, fg_color="indigo", hover_color="dark blue")
view_responses_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Run the application
root.mainloop()

# Close the database connection when done
conn.close()
