def convert_to_hertz(input_str):
    # Define the conversion factors for each prefix
    conversion_factors = {
        'Hz': 1,
        'kHz': 1e3,
        'MHz': 1e6,
        'GHz': 1e9
    }
    
    # Identify the prefix in the input string
    for prefix in conversion_factors:
        if input_str.endswith(prefix):
            number_str = input_str[:-len(prefix)]
            break
    else:
        raise ValueError("Invalid prefix. Use 'Hz', 'kHz', 'MHz', or 'GHz'.")
    
    # Convert the numeric part to a float
    number = float(number_str)
    
    # Convert the number to Hertz using the appropriate conversion factor
    return number * conversion_factors[prefix]

# Example usage
input_str = input("Enter frequency (e.g., 1000kHz): ")
hertz = convert_to_hertz(input_str)
print(f"{input_str} is {hertz} Hertz")