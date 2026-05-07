INPUT_PRICE: float = 0.50
OUTPUT_PRICE: float = 3.00
MILLION: float = 1_000_000


def calculate_costing(input_tokens: int, output_tokens: int) -> float:
    return ((input_tokens / MILLION) * INPUT_PRICE) + (
        (output_tokens / MILLION) * OUTPUT_PRICE
    )


if __name__ == "__main__":
    print(calculate_costing(200, 5000))
