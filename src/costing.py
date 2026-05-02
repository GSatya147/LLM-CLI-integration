INPUT_PRICE = 0.50
OUTPUT_PRICE = 3.00

def calculate_costing(input_tokens, output_tokens):
    return (input_tokens * INPUT_PRICE + output_tokens * OUTPUT_PRICE)

print(calculate_costing(1, 5))