from src.costing import calculate_costing

def test_input_tokens() -> None:
    result = calculate_costing(1_000_000, 0)
    assert result == 0.50

def test_output_tokens() -> None:
    result = calculate_costing(0, 1_000_000)
    assert result == 3.00

def test_zero_tokens() -> None:
    result = calculate_costing(0, 0)
    assert result == 0.0