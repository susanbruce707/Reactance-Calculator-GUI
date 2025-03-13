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
        raise ValueError("Invalid prefix. Use 'Hz', 'kHz', 'MHz', or 'GHz'.")
    
    # Convert the numeric part to a float
    try:
        number = float(number_str)
    except ValueError:
        raise ValueError("Invalid number format. Please enter a valid number.")
    
    # Convert the number to Hertz using the appropriate conversion factor
    return number * conversion_factors[prefix]

# Example usage
try:
    input_str = input("Enter frequency (e.g., '1000 kHz'): ")
    hertz = convert_to_hertz(input_str)
    print(f"{input_str} is {hertz} Hertz")
except ValueError as e:
    print(e)