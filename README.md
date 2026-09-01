# Git/GitHub Basics Assignment

This sample repository demonstrates the basic Git and GitHub workflow:

- create a local repository
- stage files with Git
- commit changes locally
- connect the repository to GitHub
- push the `main` branch to GitHub

It also includes a small Python example that makes one LLM call using the OpenAI Responses API.

## Run the LLM example

1. Install the dependency:

   ```bash
   python3 -m pip install -r requirements.txt
   ```

2. Set your API key in the environment. Never place the key directly in the source code.

   ```bash
   export OPENAI_API_KEY="your-key-here"
   ```

3. Run the program:

   ```bash
   python3 llm_call.py
   ```

The program asks the model for a one-sentence explanation of Git version control and prints the response.

