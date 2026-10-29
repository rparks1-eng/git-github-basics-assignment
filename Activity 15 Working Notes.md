# Activity 15 Working Notes

Brandon Parks

October 28, 2026

This activity compares an AI-generated commission calculator with my predictions, then revises the calculator to follow a precise rule. ChatGPT assisted with code, automated testing, and the written analysis. The predictions below are mine and were supplied before testing.

## Part 1 Prompt revisions

Original: My app is broken.

Revision: I am building a Python Streamlit sales commission calculator. When I enter a sales amount and click Calculate, the app fails instead of displaying commission. Here is my app.py and the full error message. Explain what is causing the error, suggest the smallest fix, and tell me how to check it. Ask for missing information instead of guessing.

Missing information: the framework and language, relevant code, exact error, what action causes it, expected behavior, and the runtime or package versions when relevant. This is a hypothetical revised prompt, not a claim that this calculator actually failed.

Original: I need to parse a dataset.

Revision: I have a UTF-8 CSV file of sales with columns salesperson, date, and sales_amount. Write Python code to read it, validate the required columns, convert sales_amount to numbers, and report missing or invalid values without silently dropping rows. Return a cleaned table plus an error report. Ask for a sample and clarification about date formats, currency symbols, and duplicate rows before deciding how to handle them.

Missing information: the file format and encoding, column names, example rows, desired output, field types, data size, and rules for missing, invalid, or duplicate records. This is a hypothetical dataset specification.

## Part 2 Exact one shot prompt

Build a Streamlit sales commission calculator in Python: 10% on sales up to $50,000, 15% above.

The initial app.py is saved in commit 9289e82, One-shot version. The app was tested after the predictions were supplied, using Streamlit AppTest to enter values, click Calculate, and inspect displayed output. These were automated widget tests performed by the assistant, not manual student clicks.

## Part 3 Predictions before testing

I predicted that sales above $50,000 would receive 15% on the entire amount, and that negative sales would earn no commission.

| Sales | My prediction | Observed app answer | Match |
| --- | --- | --- | --- |
| $40,000 | $4,000.00 | $4,000.00 | Yes |
| $50,000 | $5,000.00 | $5,000.00 | Yes |
| $50,001 | $7,500.15 | $5,000.15 | No |
| $80,000 | $12,000.00 | $9,500.00 | No |
| $0 | $0.00 | $0.00 | Yes |
| -$5,000 | $0.00 | -$500.00 | No |

The app matched three of six predictions. For $80,000, marginal tiers give $5,000 on the first $50,000 plus $4,500 on the remaining $30,000, totaling $9,500. A whole-amount threshold rule gives $80,000 times 15%, or $12,000. Both fit a reasonable reading of the original prompt. Negative sales were also unspecified; the initial code simply multiplied them by 10%.

At $50,000, both interpretations pay $5,000. At $50,001, marginal tiers pay $5,000.15 while the whole-amount rule pays $7,500.15. The whole-amount rule creates a $2,500.15 jump for one additional dollar in sales. A salesperson would generally prefer the higher payout above the threshold. A manager may prefer marginal tiers because costs rise gradually and the threshold does not encourage shifting sales between periods. A manager could still intentionally choose the jump as an incentive.

## Part 4 Code question log

The following AI-assisted question log examines what the initial code assumed, how it works, and what the tests reveal.

### 1 What did you assume that I did not tell you

AI answer: I assumed that 15% applies only to sales above $50,000, not the whole amount. I also accepted negative sales, used floating-point numbers, defaulted the input to zero, and displayed two decimal places without a separate currency rounding policy.

Takeaway: A short business rule can hide several decisions. The AI can make them without an obvious error message.

### 2 Can you explain how the calculation works

AI answer: Streamlit shows a number field and a Calculate button. The if statement chooses 10% for sales at or below $50,000. Above the threshold, the else branch adds $5,000 to 15% of the excess. The f-string formats the answer with commas and two decimal places.

Takeaway: The condition chooses the branch, but the formula inside that branch determines whether the rule is marginal or applies to the whole amount.

### 3 What happens with blank wrong or negative input

AI answer: The original numeric widget starts at zero and constrains normal entry to numbers. It does not separately explain a blank amount. Because no minimum is set, negative values reach the formula and produce negative commission. The revised text field deliberately distinguishes a blank entry from zero and validates it.

Takeaway: A widget's built-in input handling is not the same as having a clear business policy for invalid or unusual amounts.

### 4 What did you leave out

AI answer: The initial app does not specify currency, refunds or returns, a sales period, multiple salespeople, saved history, access control, or a maximum supported amount. It also has no independent tests. Some of these are unnecessary for a classroom calculator but would matter in a real payroll tool.

Takeaway: Running without an error does not show that every requirement has been covered. Extra features should only be added if the task needs them.

### 5 Is there a simpler way to express my rule and handle cents

AI answer: Yes. For the whole-amount interpretation, choose a rate of 10% through $50,000 or 15% above it, then multiply the entire positive sales amount by that rate. Decimal values and an explicit round-half-up policy make cent rounding predictable.

Takeaway: A precise rule can simplify the formula even when validation makes the overall code longer.

One less obvious detail in the original code is the formatting expression :,.2f. The comma adds thousands separators and .2f displays two decimal places. That makes an answer look like money, but it does not establish the correct business formula or a separate rounding policy. The rebuild uses Decimal and explicitly rounds half cents upward: $0.05 times 10% becomes $0.01. This shows why even a small formatting detail is worth asking the AI to explain.

## Part 5 Revised specification and results

The revised spec follows my predictions: once sales exceed $50,000, the whole amount receives 15%. This preserves the intended interpretation for this exercise, even though a manager might choose a smoother marginal rule in a real compensation plan. The added input-format limit and rounding policy remove decisions that the original prompt left unspecified.

Rebuild the Streamlit calculator in Python. Accept one plain US-dollar sales amount with an optional minus sign, up to 12 digits before the decimal, and at most two digits after it. Trim surrounding spaces. Reject blank input, letters, currency symbols, commas, scientific notation, nonfinite values, excessive decimal places, and amounts outside that input format with a clear message and no commission result. Do not silently turn invalid text into zero.

For sales of zero or less, return $0.00. Show an explanation when sales are negative. For positive sales through $50,000 inclusive, pay 10% of the entire amount. Above $50,000, pay 15% of the entire amount, not only the excess. Use decimal arithmetic and round to the nearest cent with half cents rounded up. State the rule visibly. Calculate when the button is clicked; when input changes, clear any previous answer so it cannot be mistaken for the new result.

Required examples: $40,000 gives $4,000.00; $50,000 gives $5,000.00; $50,001 gives $7,500.15; $80,000 gives $12,000.00; $0 gives $0.00; -$5,000 gives $0.00. These must all match the prediction table.

| Sales | Predicted commission | Revised app output | Match |
| --- | --- | --- | --- |
| $40,000 | $4,000.00 | $4,000.00 | Yes |
| $50,000 | $5,000.00 | $5,000.00 | Yes |
| $50,001 | $7,500.15 | $7,500.15 | Yes |
| $80,000 | $12,000.00 | $12,000.00 | Yes |
| $0 | $0.00 | $0.00 | Yes |
| -$5,000 | $0.00 | $0.00 | Yes |

All six revised cases passed actual Streamlit widget tests. In total, 27 checks passed: six original cases, six revised cases, ten invalid inputs, and five additional checks covering cents above the threshold, half-cent rounding, surrounding spaces, the maximum input, and clearing an outdated result. Test Results.json records the outputs; test_app.py reruns them.

## Commit comparison

The revised app and checks are saved in commit c1a1b80, Spec version. At that stage, git diff HEAD~1 compared it with the original. The same comparison remains reproducible with git diff 9289e82 c1a1b80 -- app.py. The original remains recoverable in commit 9289e82.

First, the formula changes from a marginal tier calculation to a single rate applied to the whole positive amount. This changes the two above-threshold results to match my predictions.

Second, the revised app returns zero for negative sales and explains why. It also separates blank or invalid text from a genuine zero, instead of relying only on the original number widget.

Third, the revised app uses Decimal with an explicit cent-rounding rule and adds reproducible widget tests. This checks both displayed results and error handling, rather than only whether Python runs.

## Part 6 Reflections

### What did you not know to ask the first time and how did you find out

The missing question was whether the higher rate applied to all sales or only the amount above $50,000. My predictions used the whole amount, while the initial app used marginal tiers. Comparing the outputs exposed that difference. Negative sales were another missing rule: I predicted zero, but the app returned a negative commission. Both rules need to be explicit before relying on the app.

### Why was running without errors not enough

The one-shot app ran, but three of its six answers did not match my predictions. There was no syntax error to tell us the business rule was ambiguous. Checking expected outputs showed what the app actually meant by the prompt and helped separate a programming problem from an unclear requirement. A program can run correctly according to its code and still implement the wrong policy.

### When would accepting unchecked AI code be good enough

Accepting unchecked AI code may be reasonable for a disposable, low-risk prototype that is not used to make real decisions or handle sensitive data. Its output should still be labeled unverified. A commission calculator used for real payments needs testing because an incorrect assumption can change somebody's pay. The amount of checking should increase with the consequences of being wrong.
