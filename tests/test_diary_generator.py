import pytest


ok_params = {
    "validate_args - OK case - Sample": (
        {
            "args": {"start_date": "2023-01-01", "day_range": 14},
            "expected_1": "2023-01-01",
            "expected_2": 14,
        }
    ),
    "validate_args - OK case - Date in the past": (
        {
            "args": {"start_date": "1900-05-31", "day_range": 14},
            "expected_1": "1900-05-31",
            "expected_2": 14,
        }
    ),
    "validate_args - OK case - Future date": (
        {
            "args": {"start_date": "3000-12-31", "day_range": 14},
            "expected_1": "3000-12-31",
            "expected_2": 14,
        }
    ),
    "validate_args - OK case - Generate 100 files": (
        {
            "args": {"start_date": "2023-01-01", "day_range": 100},
            "expected_1": "2023-01-01",
            "expected_2": 100,
        }
    ),
}


@pytest.mark.parametrize("params", list(ok_params.values()), ids=list(ok_params.keys()))
def test_ok_validate_args(params):
    import src.diary_generator

    actual_1, actual_2 = src.diary_generator.validate_args(params["args"])

    assert actual_1 == params["expected_1"]
    assert actual_2 == params["expected_2"]


ng_params = {
    "validate_args - NG case - Args are empty": (
        {
            "args": {"start_date": None, "day_range": None},
            "expected": "Args are empty (required two args, i.e., --start_date and --day_range)",
        }
    ),
    "validate_args - NG case - Invalid date format": (
        {
            "args": {"start_date": "20230101", "day_range": 100},
            "expected": "Date format is invalid (You must give a date, such as yyyy-mm-dd)",
        }
    ),
    "validate_args - NG case - Negative number is set to number of generate files": (
        {
            "args": {"start_date": "2023-01-01", "day_range": -100},
            "expected": "Number of days format is invalid (You must give a nonnegative integer)",
        }
    ),
}


@pytest.mark.parametrize("params", list(ng_params.values()), ids=list(ng_params.keys()))
def test_ng_validate_args(params):
    import src.diary_generator

    actual = src.diary_generator.validate_args(params["args"])

    assert actual == params["expected"]
