"""Exercise actual Streamlit widgets for both assignment versions."""

import json
from pathlib import Path
import subprocess

from streamlit.testing.v1 import AppTest


def run_checks():
    first_source = subprocess.check_output(
        ["git", "show", "9289e82:app.py"], text=True
    )
    sales_cases = [40000, 50000, 50001, 80000, 0, -5000]
    predictions = [4000, 5000, 7500.15, 12000, 0, 0]
    original_expected = [4000, 5000, 5000.15, 9500, 0, -500]
    rows = []
    for sales, prediction, original in zip(
        sales_cases, predictions, original_expected
    ):
        first = AppTest.from_string(first_source).run()
        first.number_input[0].set_value(float(sales))
        first.button[0].click().run()
        assert not first.exception
        first_display = first.markdown[0].value
        assert first_display == f"Commission: ${original:,.2f}"

        revised = AppTest.from_file("app.py").run()
        revised.text_input[0].set_value(str(sales))
        revised.button[0].click().run()
        assert not revised.exception
        revised_display = revised.markdown[0].value
        assert revised_display == f"Commission: ${prediction:,.2f}"
        if sales < 0:
            assert len(revised.warning) == 1
        rows.append({
            "sales": sales,
            "user_prediction": prediction,
            "one_shot_output": first_display,
            "one_shot_match": original == prediction,
            "spec_output": revised_display,
            "spec_match": True,
        })

    invalid_cases = ["", " ", "abc", "NaN", "inf", "1e6", "1,000", "$100", "1.234", "1000000000000"]
    for value in invalid_cases:
        app = AppTest.from_file("app.py").run()
        app.text_input[0].set_value(value)
        app.button[0].click().run()
        assert not app.exception
        assert len(app.error) == 1, value
        assert len(app.markdown) == 0, value

    for value, expected in [("50000.01", "7,500.00"), ("0.05", "0.01"), (" 40000 ", "4,000.00"), ("999999999999.99", "150,000,000,000.00")]:
        app = AppTest.from_file("app.py").run()
        app.text_input[0].set_value(value)
        app.button[0].click().run()
        assert not app.exception
        assert app.markdown[0].value == f"Commission: ${expected}"

    # Editing after a calculation must not leave a stale answer on the screen.
    app = AppTest.from_file("app.py").run()
    app.text_input[0].set_value("80000")
    app.button[0].click().run()
    assert app.markdown[0].value == "Commission: $12,000.00"
    app.text_input[0].set_value("40000").run()
    assert not app.exception
    assert len(app.markdown) == 0

    result = {
        "method": "Streamlit AppTest runs actual widget callbacks and reads rendered outputs; not a browser screenshot or manual student test.",
        "prediction_source": "Brandon supplied six predictions in chat before the first test run.",
        "one_shot_commit": "9289e82",
        "rows": rows,
        "invalid_inputs_checked": invalid_cases,
        "additional_checks": ["threshold cents", "half-up cent rounding", "surrounding spaces", "maximum supported amount", "no stale displayed answer"],
        "checks_passed": 27,
    }
    Path("Test Results.json").write_text(json.dumps(result, indent=2) + "\n")
    print("PASS: 6 original cases, 6 revised cases, 10 invalid inputs, 5 additional checks.")


if __name__ == "__main__":
    run_checks()
