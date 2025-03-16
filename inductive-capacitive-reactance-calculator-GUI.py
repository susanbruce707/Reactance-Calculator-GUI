import math
import tkinter as tk
from tkinter import messagebox, font, filedialog, ttk
from ttkthemes import ThemedTk
import os

# Define the global variable to store the last result
last_result = None
recent_calculations_file = "recent_calculations.txt"

def convert_to_units(input_str, conversion_factors):
    input_str = input_str.lower().replace(" ", "")  # Remove spaces
    for prefix, factor in conversion_factors.items():
        if (input_str.endswith(prefix)):
            number_str = input_str[:-len(prefix)]
            if not number_str.replace('.', '', 1).isdigit():
                raise ValueError("Invalid number format. Please enter a valid number.")
            try:
                number = float(number_str)
                return number * factor
            except ValueError:
                raise ValueError("Invalid number format. Please enter a valid number.")
    raise ValueError(f"Invalid prefix. Use one of {', '.join(conversion_factors.keys())}.")

def convert_to_hertz(input_str):
    conversion_factors = {'hz': 1, 'khz': 1e3, 'mhz': 1e6, 'ghz': 1e9}
    return convert_to_units(input_str, conversion_factors)

def convert_to_farads(input_str):
    conversion_factors = {'pf': 1e-12, 'nf': 1e-9, 'uf': 1e-6, 'mf': 1e-3, 'kf': 1e3}
    return convert_to_units(input_str, conversion_factors)

def convert_to_henrys(input_str):
    conversion_factors = {'ph': 1e-12, 'nh': 1e-9, 'uh': 1e-6, 'mh': 1e-3, 'h': 1}
    return convert_to_units(input_str, conversion_factors)

def calculate_inductive_reactance(frequency, inductance):
    return 2 * math.pi * frequency * inductance

def calculate_capacitive_reactance(frequency, capacitance):
    return 1 / (2 * math.pi * frequency * capacitance)

def calculate_total_reactance(frequency, inductance, capacitance):
    inductive_reactance = calculate_inductive_reactance(frequency, inductance)
    capacitive_reactance = calculate_capacitive_reactance(frequency, capacitance)
    total_reactance = inductive_reactance - capacitive_reactance
    return inductive_reactance, capacitive_reactance, total_reactance

def calculate_and_display_reactance():
    global last_result
    try:
        freq_input = frequency_entry.get().strip()
        if not freq_input:
            raise ValueError("Frequency input is required.")
        frequency = convert_to_hertz(freq_input)
        
        if reactance_type.get() == "Inductive":
            ind_input = inductance_entry.get().strip()
            if not ind_input:
                raise ValueError("Inductance input is required.")
            inductance = convert_to_henrys(ind_input)
            reactance = calculate_inductive_reactance(frequency, inductance)
            last_result = f"The inductive reactance for {freq_input} and {ind_input} is {reactance:.2f} Ohms\n"
        elif reactance_type.get() == "Capacitive":
            cap_input = capacitance_entry.get().strip()
            if not cap_input:
                raise ValueError("Capacitance input is required.")
            capacitance = convert_to_farads(cap_input)
            reactance = calculate_capacitive_reactance(frequency, capacitance)
            last_result = f"The capacitive reactance for {freq_input} and {cap_input} is {reactance:.2f} Ohms\n"
        else:  # Both Ind&Cap
            ind_input = inductance_entry.get().strip()
            cap_input = capacitance_entry.get().strip()
            if not ind_input or not cap_input:
                raise ValueError("Both inductance and capacitance inputs are required.")
            inductance = convert_to_henrys(ind_input)
            capacitance = convert_to_farads(cap_input)
            inductive_reactance, capacitive_reactance, total_reactance = calculate_total_reactance(frequency, inductance, capacitance)
            reactance_type_str = "inductive" if total_reactance > 0 else "capacitive"
            last_result = (f"The inductive reactance for {freq_input} and {ind_input} is {inductive_reactance:.2f} Ohms\n"
                           f"The capacitive reactance for {freq_input} and {cap_input} is {capacitive_reactance:.2f} Ohms\n"
                           f"The total reactance is {abs(total_reactance):.2f} Ohms {reactance_type_str}\n")
        
        result_label.config(text=last_result)
        results_text_box.insert(tk.END, last_result + "\n")
        status_label.config(text="Calculation successful", foreground="green")
        add_to_recent_calculations(last_result + "\n")
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))
        status_label.config(text="Error in input", foreground="red")

def validate_frequency_entry(event):
    try:
        freq_input = frequency_entry.get().strip()
        if not freq_input:
            raise ValueError("Frequency input is required.")
        convert_to_hertz(freq_input)
        if reactance_type.get() == "Inductive":
            inductance_entry.focus_set()
        elif reactance_type.get() == "Capacitive":
            capacitance_entry.focus_set()
        else:
            inductance_entry.focus_set()
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

def validate_inductance_entry(event):
    try:
        ind_input = inductance_entry.get().strip()
        if not ind_input:
            raise ValueError("Inductance input is required.")
        convert_to_henrys(ind_input)
        if reactance_type.get() == "Both Ind&Cap":
            capacitance_entry.focus_set()
        else:
            calculate_and_display_reactance()
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

def validate_capacitance_entry(event):
    try:
        cap_input = capacitance_entry.get().strip()
        if not cap_input:
            raise ValueError("Capacitance input is required.")
        convert_to_farads(cap_input)
        calculate_and_display_reactance()
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

def save_result_to_file():
    results_text = results_text_box.get("1.0", tk.END).strip()
    if results_text:
        with open("reactance_results.txt", "a") as file:
            file.write(results_text + "\n")
        messagebox.showinfo("Save Successful", "The results have been saved to reactance_results.txt")
    else:
        messagebox.showwarning("Save Warning", "No results to save. Please perform a calculation or enter text first.")

def save_result_as():
    results_text = results_text_box.get("1.0", tk.END).strip()
    if results_text:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(results_text + "\n")
            messagebox.showinfo("Save Successful", f"The results have been saved to {file_path}")
    else:
        messagebox.showwarning("Save Warning", "No results to save. Please perform a calculation or enter text first.")

def show_about():
    messagebox.showinfo("About", "Reactance Calculator\nVersion 1.0\nDeveloped by Susan\n\nThis application calculates the reactance of inductors and capacitors based on the input frequency, inductance, and capacitance values. You can save the results to a file for future reference.")

def clear_entries():
    frequency_entry.delete(0, tk.END)
    inductance_entry.delete(0, tk.END)
    capacitance_entry.delete(0, tk.END)
    result_label.config(text="")
    frequency_entry.focus_set()
    status_label.config(text="Entries cleared", fg="blue")

def clear_results():
    results_text_box.delete("1.0", tk.END)
    status_label.config(text="Results cleared", fg="blue")

def create_tooltip(widget, text):
    # Create a Toplevel window to act as the tooltip
    tooltip = tk.Toplevel(widget)
    tooltip.wm_overrideredirect(True)  # Remove window decorations
    tooltip.withdraw()  # Hide the tooltip initially
    label = tk.Label(tooltip, text=text, bg="yellow", relief="solid", borderwidth=1, wraplength=150)
    label.pack()

    def show_tooltip(event):
        # Position the tooltip at the mouse pointer location
        x = event.x_root + 10
        y = event.y_root + 10
        tooltip.wm_geometry(f"+{x}+{y}")
        tooltip.deiconify()  # Show the tooltip

    def hide_tooltip(event):
        # Hide the tooltip
        tooltip.withdraw()

    # Bind the Enter and Leave events to show and hide the tooltip
    widget.bind("<Enter>", show_tooltip)
    widget.bind("<Leave>", hide_tooltip)

def update_entry_state():
    if reactance_type.get() == "Both Ind&Cap":
        inductance_entry.config(state=tk.NORMAL)
        capacitance_entry.config(state=tk.NORMAL)
    elif reactance_type.get() == "Inductive":
        inductance_entry.config(state=tk.NORMAL)
        capacitance_entry.config(state=tk.DISABLED)
    else:
        inductance_entry.config(state=tk.DISABLED)
        capacitance_entry.config(state=tk.NORMAL)

def reset_form():
    frequency_entry.delete(0, tk.END)
    inductance_entry.delete(0, tk.END)
    capacitance_entry.delete(0, tk.END)
    frequency_entry.insert(0, "1000 Hz")
    inductance_entry.insert(0, "1000 uH")
    capacitance_entry.config(state=tk.DISABLED)
    reactance_type.set("Inductive")
    result_label.config(text="")
    status_label.config(text="Form reset to initial state", foreground="blue")
    # Save recent calculations and clear the recent calculations list
    save_recent_calculations()
    recent_calculations_list.delete(0, tk.END)

def add_to_recent_calculations(result):
    # Split the result into individual lines and add each line separately
    for line in result.strip().split('\n'):
        recent_calculations_list.insert(tk.END, line)
    save_recent_calculations()

def save_recent_calculations():
    with open(recent_calculations_file, "w") as file:
        for item in recent_calculations_list.get(0, tk.END):
            # Ensure each item is properly formatted before saving
            file.write(item.strip() + "\n")

def load_recent_calculations():
    if os.path.exists(recent_calculations_file):
        with open(recent_calculations_file, "r") as file:
            for line in file:
                recent_calculations_list.insert(tk.END, line.strip())

def set_light_theme():
    root.set_theme('arc')
    root.configure(bg='white')
    results_text_box.configure(bg='white', fg='black')
    recent_calculations_list.configure(bg='white', fg='black')
    root.title("Reactance Calculator - Light Mode")

def set_dark_theme():
    root.set_theme('equilux')
    root.configure(bg='black')
    results_text_box.configure(bg='black', fg='white')
    recent_calculations_list.configure(bg='black', fg='white')
    root.title("Reactance Calculator - Dark Mode")

def on_closing():
    save_recent_calculations()
    root.destroy()

# Create the main window using ThemedTk
root = ThemedTk(theme="arc")
root.title("Reactance Calculator - Light Mode")
root.configure(bg='white')

# Create a style object
style = ttk.Style()

# Create the menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create the file menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Save Results", command=save_result_to_file)
file_menu.add_command(label="Save Results As...", command=save_result_as)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=on_closing)
menu_bar.add_cascade(label="File", menu=file_menu)

# Create the settings menu
settings_menu = tk.Menu(menu_bar, tearoff=0)
settings_menu.add_command(label="Light Theme", command=set_light_theme)
settings_menu.add_command(label="Dark Theme", command=set_dark_theme)
menu_bar.add_cascade(label="Settings", menu=settings_menu)

# Create the help menu
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menu_bar.add_cascade(label="Help", menu=help_menu)

# Create and place the frequency input widgets
ttk.Label(root, text="Enter frequency (e.g., '1000 Hz,khz,mhz'):").grid(row=1, column=0, padx=10, pady=10, sticky="e")
frequency_entry = ttk.Entry(root)
frequency_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
frequency_entry.insert(0, "1000 Hz")  # Set default value
frequency_entry.bind("<Return>", validate_frequency_entry)
create_tooltip(frequency_entry, "Enter the frequency in Hz, kHz, MHz, or GHz")

# Create and place the reactance type radio buttons in a frame
reactance_frame = ttk.Frame(root)
reactance_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

reactance_type = tk.StringVar(value="Inductive")
ttk.Radiobutton(reactance_frame, text="Inductive", variable=reactance_type, value="Inductive", command=update_entry_state).pack(side=tk.LEFT, padx=5)
ttk.Radiobutton(reactance_frame, text="Both Ind&Cap", variable=reactance_type, value="Both Ind&Cap", command=update_entry_state).pack(side=tk.LEFT, padx=5)
ttk.Radiobutton(reactance_frame, text="Capacitive", variable=reactance_type, value="Capacitive", command=update_entry_state).pack(side=tk.LEFT, padx=5)

# Create and place the inductance input widgets
ttk.Label(root, text="Enter inductance (e.g., '1000 uH,mh'):").grid(row=3, column=0, padx=10, pady=10, sticky="e")
inductance_entry = ttk.Entry(root)
inductance_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")
inductance_entry.insert(0, "1000 uH")  # Set default value
inductance_entry.bind("<Return>", validate_inductance_entry)
create_tooltip(inductance_entry, "Enter the inductance in uH, mH, or H")

# Create and place the capacitance input widgets
ttk.Label(root, text="Enter capacitance (e.g., '1000 pF,nf,uf'):").grid(row=4, column=0, padx=10, pady=10, sticky="e")
capacitance_entry = ttk.Entry(root)
capacitance_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")
capacitance_entry.bind("<Return>", validate_capacitance_entry)
create_tooltip(capacitance_entry, "Enter the capacitance in pF, nF, or uF")

# Initially disable the capacitance entry
capacitance_entry.config(state=tk.DISABLED)

# Create and place the calculate button
calculate_button = ttk.Button(root, text="Calculate Reactance", command=calculate_and_display_reactance)
calculate_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
create_tooltip(calculate_button, "Click to calculate the reactance")

# Create and place the next calculation button
next_calculation_button = ttk.Button(root, text="Next Calculation", command=clear_entries)
next_calculation_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
create_tooltip(next_calculation_button, "Click to clear the entries for the next calculation")

# Create and place the reset button
reset_button = ttk.Button(root, text="Reset", command=reset_form)
reset_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
create_tooltip(reset_button, "Click to reset the form to its initial state")

# Create and place the result label with a heading and outline
result_frame = ttk.Frame(root, relief=tk.SUNKEN)
result_frame.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

ttk.Label(result_frame, text="Results:", font=('Arial', 12, 'bold')).pack(anchor='nw', padx=5, pady=5)
result_label = ttk.Label(result_frame, text="")
result_label.pack(padx=5, pady=5)

# Create and place the save result button, clear results button, and close app button on the same line
button_frame = ttk.Frame(root)
button_frame.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

save_button = ttk.Button(button_frame, text="Save Result", command=save_result_to_file)
save_button.pack(side=tk.LEFT, padx=5)
create_tooltip(save_button, "Click to save the result to a file")

clear_results_button = ttk.Button(button_frame, text="Clear Results", command=clear_results)
clear_results_button.pack(side=tk.LEFT, padx=5)
create_tooltip(clear_results_button, "Click to clear the results text box")

close_button = ttk.Button(button_frame, text="Close", command=on_closing)
close_button.pack(side=tk.LEFT, padx=5)
create_tooltip(close_button, "Click to close the application")

# Create and place the results text box with a heading and outline
results_frame = ttk.Frame(root, relief=tk.SUNKEN)
results_frame.grid(row=0, column=2, rowspan=10, padx=10, pady=10, sticky="nsew")

ttk.Label(results_frame, text="Results:", font=('Arial', 12, 'bold')).pack(anchor='nw', padx=5, pady=5)
results_text_box = tk.Text(results_frame, width=60, height=20, wrap=tk.WORD, bg='white', fg='black')
results_text_box.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

# Add a scrollbar to the results text box
scrollbar = ttk.Scrollbar(results_frame, command=results_text_box.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
results_text_box.config(yscrollcommand=scrollbar.set)

# Set a smaller font for the results text box
small_font = font.Font(size=10)
results_text_box.configure(font=small_font)

# Create and place the recent calculations list
recent_calculations_frame = ttk.Frame(root, relief=tk.SUNKEN)
recent_calculations_frame.grid(row=0, column=3, rowspan=10, padx=10, pady=10, sticky="nsew")

ttk.Label(recent_calculations_frame, text="Recent Calculations:", font=('Arial', 12, 'bold')).pack(anchor='nw', padx=5, pady=5)
recent_calculations_list = tk.Listbox(recent_calculations_frame, width=60, height=20, bg='white', fg='black')
recent_calculations_list.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

# Add a scrollbar to the recent calculations list
recent_calculations_scrollbar = ttk.Scrollbar(recent_calculations_frame, command=recent_calculations_list.yview)
recent_calculations_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
recent_calculations_list.config(yscrollcommand=recent_calculations_scrollbar.set)

# Create and place the status bar
status_label = ttk.Label(root, text="", relief=tk.SUNKEN, anchor=tk.W)
status_label.grid(row=10, column=0, columnspan=4, sticky="ew")

# Load recent calculations
load_recent_calculations()

# Run the main event loop
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()