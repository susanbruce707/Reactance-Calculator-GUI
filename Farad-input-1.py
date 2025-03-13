def convert_to_farads(input_str):
    # Split the input string into the numeric part and the prefix
    number_str, prefix = input_str[:-2], input_str[-2:]
    
    # Convert the numeric part to a float
    number = float(number_str)
    
    # Define the conversion factors for each prefix
    conversion_factors = {
        'pf': 1e-12,
        'nf': 1e-9,
        'uf': 1e-6,
        'mf': 1e-3,
        'kf': 1e3
    }
    
    # Convert the number to Farads using the appropriate conversion factor
    if prefix in conversion_factors:
        return number * conversion_factors[prefix]
    else:
        raise ValueError("Invalid prefix. Use 'pf', 'nf', or 'uf'.")

# Example usage
input_str = input("1000pf example ")
farads = convert_to_farads(input_str)
print(f"{input_str} is {farads} Farads")