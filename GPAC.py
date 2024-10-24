import json
import os
import customtkinter as ctk

class GPACalculator:
    def __init__(self, filename='subjects.json'):
        self.subjects = {}
        self.filename = filename
        self.load_subjects()

    def add_subject(self, subject_name):
        if subject_name in self.subjects:
            self.custom_messagebox("Error", f"{subject_name} is already added.")
        else:
            self.subjects[subject_name] = {'credits': 0, 'grade': None}
            self.save_subjects()

    def convert_grade_to_points(self, grade):
        grade_scale = {
            'A+': 10, 'A': 9, 'B+': 8, 'B': 7,
            'C+': 6, 'C': 5, 'D': 4, 'F': 0
        }
        return grade_scale.get(grade.upper(), None)

    def calculate_gpa(self, subject_name, credits, grade):
        if subject_name in self.subjects:
            self.subjects[subject_name]['credits'] = credits
            self.subjects[subject_name]['grade'] = self.convert_grade_to_points(grade)

            total_credits = sum(data['credits'] for data in self.subjects.values())
            total_points = sum(data['credits'] * data['grade'] for data in self.subjects.values() if data['grade'] is not None)

            if total_credits == 0:
                self.custom_messagebox("Warning", "No valid subjects added.")
                return None

            gpa = total_points / total_credits
            return round(gpa, 2)
        else:
            self.custom_messagebox("Error", f"{subject_name} is not in the list.")

    def save_subjects(self):
        with open(self.filename, 'w') as f:
            json.dump(self.subjects, f)

    def load_subjects(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.subjects = json.load(f)

    def custom_messagebox(self, title, message):
        messagebox_window = ctk.CTkToplevel()
        messagebox_window.title(title)
        messagebox_window.geometry("300x150")

        # Add a label with the message
        message_label = ctk.CTkLabel(messagebox_window, text=message)
        message_label.pack(pady=20)

        # Add a button to close the window
        ok_button = ctk.CTkButton(messagebox_window, text="OK", command=messagebox_window.destroy)
        ok_button.pack(pady=10)

# Creating the GUI using customtkinter
class GPACalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GPA Calculator")
        self.calculator = GPACalculator()

        # Configure theme and appearance
        ctk.set_appearance_mode("System")  # Options: "System", "Light", "Dark"
        ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

        # Buttons
        ctk.CTkButton(root, text="Add Subject", command=self.open_add_subject_window).grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkButton(root, text="Calculate CGPA", command=self.open_calculate_gpa_window).grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkButton(root, text="View Subjects", command=self.view_subjects).grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Quit button
        ctk.CTkButton(root, text="Quit", command=root.quit).grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def open_add_subject_window(self):
        add_subject_window = ctk.CTkToplevel(self.root)
        add_subject_window.title("Add Subject")

        # Subject Name Input
        ctk.CTkLabel(add_subject_window, text="Subject Name:").grid(row=0, column=0, padx=10, pady=10)
        subject_entry = ctk.CTkEntry(add_subject_window)
        subject_entry.grid(row=0, column=1, padx=10, pady=10)

        # Save Button
        ctk.CTkButton(add_subject_window, text="Save", command=lambda: self.save_subject(subject_entry.get(), add_subject_window)).grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def save_subject(self, subject_name, window):
        if subject_name:
            self.calculator.add_subject(subject_name)
            self.calculator.custom_messagebox("Success", f"Added {subject_name} successfully.")
            window.destroy()  # Close the add subject window
        else:
            self.calculator.custom_messagebox("Error", "Please enter a valid subject name.")

    def open_calculate_gpa_window(self):
        calculate_window = ctk.CTkToplevel(self.root)
        calculate_window.title("Calculate CGPA")

        # Subject Selection
        ctk.CTkLabel(calculate_window, text="Select Subject:").grid(row=0, column=0, padx=10, pady=10)
        subject_entry = ctk.CTkEntry(calculate_window)
        subject_entry.grid(row=0, column=1, padx=10, pady=10)

        # Credits Input
        ctk.CTkLabel(calculate_window, text="Credits:").grid(row=1, column=0, padx=10, pady=10)
        credits_entry = ctk.CTkEntry(calculate_window)
        credits_entry.grid(row=1, column=1, padx=10, pady=10)

        # Grade Input
        ctk.CTkLabel(calculate_window, text="Grade (A+, A, B+, etc.):").grid(row=2, column=0, padx=10, pady=10)
        grade_entry = ctk.CTkEntry(calculate_window)
        grade_entry.grid(row=2, column=1, padx=10, pady=10)

        # Calculate Button
        ctk.CTkButton(calculate_window, text="Calculate", command=lambda: self.calculate_cgpa(subject_entry.get(), credits_entry.get(), grade_entry.get(), calculate_window)).grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def calculate_cgpa(self, subject_name, credits, grade, window):
        try:
            credits = int(credits)
            if subject_name and grade:
                gpa = self.calculator.calculate_gpa(subject_name, credits, grade)
                if gpa is not None:
                    self.calculator.custom_messagebox("CGPA", f"Your CGPA is: {gpa}")
                window.destroy()  # Close the calculate window
            else:
                self.calculator.custom_messagebox("Error", "Please enter a valid subject name, credits, and grade.")
        except ValueError:
            self.calculator.custom_messagebox("Error", "Invalid input. Please enter valid credits.")

    def view_subjects(self):
        subjects = self.calculator.subjects
        if not subjects:
            self.calculator.custom_messagebox("No Subjects", "No subjects added yet.")
        else:
            view_window = ctk.CTkToplevel(self.root)
            view_window.title("Subjects List")

            ctk.CTkLabel(view_window, text="Subject Name").grid(row=0, column=0, padx=10, pady=5)
            for i, subject_name in enumerate(subjects.keys(), start=1):
                ctk.CTkLabel(view_window, text=subject_name).grid(row=i, column=0, padx=10, pady=5)


# Running the application
if __name__ == "__main__":
    root = ctk.CTk()
    app = GPACalculatorApp(root)
    root.mainloop()
