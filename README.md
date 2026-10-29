# Activity 15 Sales Commission Calculator

Brandon Parks

`Answers.docx` is the answer document. It includes the original prompts,
Brandon's predictions supplied before testing, original and rebuilt results,
five code questions, the precise rebuild specification, and reflections.
Code, automated testing, and written analysis used ChatGPT assistance.

## Run

```bash
uv sync
uv run streamlit run app.py --server.address 127.0.0.1
```

Run the reproducible widget tests:

```bash
uv run python test_app.py
```

The checks use Streamlit AppTest, not fabricated screenshots or claimed manual
clicks. The 27 checks cover both versions, all six assignment inputs, invalid
input, cents and rounding, the supported maximum, and stale displayed answers.

## Versions

- `9289e82` is the original `One-shot version`.
- `c1a1b80` is the rebuilt `Spec version`.
- Compare the calculator code with `git diff 9289e82 c1a1b80 -- app.py`.

The final calculator follows the whole-amount interpretation: 10% through
$50,000 and 15% of the entire positive amount above it. Nonpositive sales earn
zero commission. It intentionally retains the threshold jump discussed in
the answer document; this is not a production payroll application.

The Markdown notes are the document source. `build_answers.py` rebuilds the
existing Word file and requires `python-docx` in the document-authoring runtime.
