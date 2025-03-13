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

def convert_to_henrys(input_str):
    # Define the conversion factors for each prefix
    conversion_factors = {
        'ph': 1e-12,
        'nh': 1e-9,
        'uh': 1e-6,
        'mh': 1e-3,
        'h': 1
    }
    
    # Convert the input string to lowercase
    input_str = input_str.lower()
    
    # Split the input string into the numeric part and the prefix
    if input_str[-2:] in conversion_factors:
        number_str, prefix = input_str[:-2], input_str[-2:]
    elif input_str[-1:] in conversion_factors:
        number_str, prefix = input_str[:-1], input_str[-1:]
    else:
        raise ValueError("Invalid prefix. Use 'pH', 'nH', 'uH', 'mH', or 'H'.")
    
    # Convert the numeric part to a float
    try:
        number = float(number_str)
    except ValueError:
        raise ValueError("Invalid number format. Please enter a valid number.")
    
    # Convert the number to Henrys using the appropriate conversion factor
    return number * conversion_factors[prefix]

def calculate_inductive_reactance(frequency, inductance):
    # Calculate the inductive reactance using the formula X_L = 2 * pi * f * L
    reactance = 2 * math.pi * frequency * inductance
    return reactance

def calculate_and_display_reactance():
    try:
        freq_input = frequency_entry.get()
        frequency = convert_to_hertz(freq_input)
        
        ind_input = inductance_entry.get()
        inductance = convert_to_henrys(ind_input)
        
        reactance = calculate_inductive_reactance(frequency, inductance)
        result_label.config(text=f"The inductive reactance for {freq_input} and {ind_input} is {reactance:.2f} Ohms")
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

# Create the main window
root = tk.Tk()
root.title("Inductive Reactance Calculator")

# Create and place the frequency input widgets
tk.Label(root, text="Enter frequency (e.g., '1000 kHz'):").grid(row=0, column=0, padx=10, pady=10)
frequency_entry = tk.Entry(root)
frequency_entry.grid(row=0, column=1, padx=10, pady=10)

# Create and place the inductance input widgets
tk.Label(root, text="Enter inductance (e.g., '1000 uH'):").grid(row=1, column=0, padx=10, pady=10)
inductance_entry = tk.Entry(root)
inductance_entry.grid(row=1, column=1, padx=10, pady=10)

# Create and place the calculate button
calculate_button = tk.Button(root, text="Calculate Inductive Reactance", command=calculate_and_display_reactance)
calculate_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Create and place the result label
result_label = tk.Label(root, text="")
result_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Run the main event loop
root.mainloop()