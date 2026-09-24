# Stage 5: The Retry Loop -> make validation fail, then have Claude fix it's own mistake.

import anthropic
from dotenv import load_dotenv
import os, json, re
from pydantic import BaseModel, ValidationError

load_dotenv()
client = anthropic.Client(api_key=os.environ["ANTHROPIC_API_KEY"])

# Schema now requires a phone_number - we'll forget to ask for it so validation fails first
class Person(BaseModel):
    name: str
    age: int
    email: str
    phone_number: str   # required, but our prompt won't mention it at first

# Helper: pull JSON out of Claude's text and validate it. Returns (person, error).
def try_get_person(raw_text):
    match = re.search(r'\{[\s\S]*\}', raw_text)
    if not match:
        return None, "No JSON object found in the response."
    try: 
        data = json.loads(match.group(0))
    except json.JSONDecodeError as e:
        return None, f"Invalid JSON: {e}"
    try:
        return Person(**data), None     # success: return the person, no error
    except ValidationError as e:
        return None, str(e)     # failure: return the error message as text

messages = [{
    "role" : "user",
    "content" : "Give me a fictional person as JSON with fields: name, age, email. Return ONLY the JSON object."
}]

max_retries = 3
attempt = 0

while attempt < max_retries:
    attempt += 1
    print(f"\n--- Attempt {attempt} ---")

    response = client.messages.create(
        model = "claude-sonnet-4-6",
        max_tokens = 1024,
        messages = messages
    )
    raw_text = response.content[0].text
    print("Claude returned: ", raw_text)

    person, error = try_get_person(raw_text)

    if person:      # validation passed - we're done
        print("\n✅ Valid person: ", person)
        break

    # Validation failed - send the error BACK to Claude and ask it to fix it
    print("\n❌ Validation failed: ", error)
    messages.append({"role" : "assistant", "content" : raw_text})   # add Claude's bad answer
    messages.append({       # add our correction request
        "role" : "user",
        "content" : f"That failed validation with this error: \n{error}\nPlease fix it and return ONLY the corrected JSON object."
    })
else:
    print("\n⚠️ Gave up after max retries.")

