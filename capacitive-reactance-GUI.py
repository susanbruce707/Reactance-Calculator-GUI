import math
import tkinter as tk
from tkinter import messagebox

def convert_to_hertz(input_str):
    # Define the conversion factors for each prefix
    conversion_factors = {
        'hz': 1,
        'khz': 1e3,
        'mhz': 1e6,
        'ghz': 1e9
    }
    
    # Convert the input string to lowercase
    input_str = input_str.lower()
    
    # Split the input string into the numeric part and the prefix
    if input_str[-3:] in conversion_factors:
        number_str, prefix = input_str[:-3], input_str[-3:]
    elif input_str[-2:] in conversion_factors:
        number_str, prefix = input_str[:-2], input_str[-2:]
    else:
        raise ValueError("Invalid prefix. Use upper or lower case 'Hz', 'kHz', 'MHz', or 'GHz'.")
    
    # Convert the numeric part to a float
    try:
        number = float(number_str)
    except ValueError:
        raise ValueError("Invalid number format. Please enter a valid number.")
    
    # Convert the number to Hertz using the appropriate conversion factor
    return number * conversion_factors[prefix]

def convert_to_farads(input_str):
    # Define the conversion factors for each prefix
    conversion_factors = {
        'pf': 1e-12,
        'nf': 1e-9,
        'uf': 1e-6,
        'mf': 1e-3,
        'kf': 1e3
    }
    
    # Convert the input string to lowercase
    input_str = input_str.lower()
    
    # Split the input string into the numeric part and the prefix
    if input_str[-2:] in conversion_factors:
        number_str, prefix = input_str[:-2], input_str[-2:]
    elif input_str[-3:] in conversion_factors:
        number_str, prefix = input_str[:-3], input_str[-3:]
    else:
        raise ValueError("Invalid prefix. Use 'pf', 'nf', 'uf', 'mf', or 'kf'.")
    
    # Convert the numeric part to a float
    try:
        number = float(number_str)
    except ValueError:
        raise ValueError("Invalid number format. Please enter a valid number.")
    
    # Convert the number to Farads using the appropriate conversion factor
    return number * conversion_factors[prefix]

def calculate_reactance(frequency, capacitance):
    # Calculate the reactance using the formula Xc = 1 / (2 * pi * f * C)
    reactance = 1 / (2 * math.pi * frequency * capacitance)
    return reactance

def calculate_and_display_reactance():
    try:
        freq_input = frequency_entry.get()
        frequency = convert_to_hertz(freq_input)
        
        cap_input = capacitance_entry.get()
        capacitance = convert_to_farads(cap_input)
        
        reactance = calculate_reactance(frequency, capacitance)
        result_label.config(text=f"The reactance for {freq_input} and {cap_input} is {reactance:.2f} Ohms")
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

# Create the main window
root = tk.Tk()
root.title("Reactance Calculator")

# Create and place the frequency input widgets
tk.Label(root, text="Enter frequency (e.g., '1000 kHz'):").grid(row=0, column=0, padx=10, pady=10)
frequency_entry = tk.Entry(root)
frequency_entry.grid(row=0, column=1, padx=10, pady=10)

# Create and place the capacitance input widgets
tk.Label(root, text="Enter capacitance (e.g., '1000 pF'):").grid(row=1, column=0, padx=10, pady=10)
capacitance_entry = tk.Entry(root)
capacitance_entry.grid(row=1, column=1, padx=10, pady=10)

# Create and place the calculate button
calculate_button = tk.Button(root, text="Calculate Reactance", command=calculate_and_display_reactance)
calculate_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Create and place the result label
result_label = tk.Label(root, text="")
result_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Run the main event loop
root.mainloop()