"""A minimal LLM call using the OpenAI Responses API."""

import os

from openai import OpenAI


def main() -> None:
    """Send one prompt to an LLM and print its response."""
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit(
            "OPENAI_API_KEY is not set. Add it to your environment before running."
        )

    client = OpenAI()
    response = client.responses.create(
        model="gpt-5-mini",
        input="Explain Git version control in one clear sentence.",
    )
    print(response.output_text)


if __name__ == "__main__":
    main()

