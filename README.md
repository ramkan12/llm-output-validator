# Validate + Retry

A Python script that gets structured JSON from Claude, validates it against a Pydantic schema, and sends the validation errors back to Claude so it can fix its own output.

## What it demonstrates

- **Structured output validation:** a Pydantic `Person` model sets the exact shape and types the LLM output must match.
- **Defensive parsing:** a regex pulls the `{...}` block out of Claude's reply, which handles markdown code fences and extra text. Bad JSON is caught instead of crashing the script.
- **Retry on failure with error feedback:** the specific validation error is added to the conversation so Claude can correct the response itself.
- **Safety cap:** the loop stops after 3 attempts rather than retrying forever.

## How it works

The project is built in five stages, one file each. Stages 1 to 3 define the `Person` model, feed it broken data on purpose, and catch the `ValidationError` cleanly. Stage 4 asks Claude for a person as JSON, extracts and parses it, and validates it. Stage 5 adds a required `phone_number` field that the prompt leaves out, so the first attempt fails. Claude's bad answer and the exact Pydantic error go back into the message history as a new user turn asking for a fix. The loop repeats until the output validates or the retry cap is reached.

## Built from scratch

This project uses the Anthropic SDK and Pydantic directly, with no agent framework such as LangChain or Instructor. I built it this way on purpose, to understand the validate, feed back and retry cycle that those frameworks handle for you.

## Run it

```bash
pip install anthropic pydantic python-dotenv
```

Create a `.env` file in this folder with your own key:

```
ANTHROPIC_API_KEY=your-key-here
```

Then run any stage. Stage 5 is the full retry loop:

```bash
python stage5.py
```

## Tech used

Python, Anthropic API (Claude), Pydantic, python-dotenv
