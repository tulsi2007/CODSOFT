import tkinter as tk
from tkinter import ttk, messagebox
import random
import string

# Constants
APP_WIDTH = 500
APP_HEIGHT = 400
MAX_LENGTH = 80

# Character sets
CHARACTER_SETS = {
    "lowercase": string.ascii_lowercase,
    "uppercase": string.ascii_uppercase,
    "digits": string.digits,
    "special": string.punctuation
}

# Password generator logic
def generate_password(length, strength):
    selected_sets = []

    if strength == "low":
        selected_sets = ["lowercase", "digits"]
    elif strength == "medium":
        selected_sets = ["lowercase", "uppercase", "digits"]
    elif strength == "high":
        selected_sets = ["lowercase", "uppercase", "digits", "special"]

    if length < len(selected_sets):
        raise ValueError("Password length too short for selected strength.")

    all_chars = []
    guaranteed = []

    for set_name in selected_sets:
        chars = CHARACTER_SETS[set_name]
        all_chars += chars
        guaranteed.append(random.choice(chars))

    remaining_length = length - len(guaranteed)
    remaining_chars = [random.choice(all_chars) for _ in range(remaining_length)]

    password_chars = guaranteed + remaining_chars
    random.shuffle(password_chars)

    return ''.join(password_chars)

# UI setup
def setup_ui(root):
    root.title("Password Generator")
    root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
    root.resizable(False, False)

    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(fill=tk.BOTH, expand=True)

    # Heading
    tk.Label(frame, text="Password Generator", font=("Arial", 20, "bold")).pack(pady=(0, 20))

    # Password length
    length_frame = tk.Frame(frame)
    length_frame.pack(anchor="w", pady=5)
    tk.Label(length_frame, text="Length:", font=("Arial", 12)).pack(side="left")
    length_entry = tk.Entry(length_frame, width=5, font=("Arial", 12))
    length_entry.pack(side="left", padx=(10, 0))

    # Strength selection
    strength_frame = tk.Frame(frame)
    strength_frame.pack(anchor="w", pady=5)
    tk.Label(strength_frame, text="Strength:", font=("Arial", 12)).pack(side="left")

    strength_var = tk.StringVar(value="high")
    for label, val in [("Low", "low"), ("Medium", "medium"), ("High", "high")]:
        ttk.Radiobutton(strength_frame, text=label, variable=strength_var, value=val).pack(side="left", padx=10)

    # Output
    output_label = tk.Label(frame, text="Generated Password:", font=("Arial", 12))
    output_label.pack(anchor="w", pady=(15, 0))

    password_entry = tk.Entry(frame, font=("Courier New", 12), width=40, state="readonly")
    password_entry.pack(pady=(0, 15))

    # Generate button
    def on_generate():
        try:
            length = int(length_entry.get())
            if length < 4 or length > MAX_LENGTH:
                raise ValueError("Password length must be between 4 and 80.")
            strength = strength_var.get()
            password = generate_password(length, strength)
            password_entry.config(state="normal")
            password_entry.delete(0, tk.END)
            password_entry.insert(0, password)
            password_entry.config(state="readonly")
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")

    tk.Button(frame, text="Generate Password", font=("Arial", 12), command=on_generate).pack(pady=10)

# Main function
if __name__ == "__main__":
    app = tk.Tk()
    setup_ui(app)
    app.mainloop()

