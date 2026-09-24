# Stage 4: Wire in the LLM

import anthropic
from dotenv import load_dotenv
import os
import re       # regex
import json     # to parse JSON into a Python dictionary
from pydantic import BaseModel, ValidationError     

load_dotenv()

client = anthropic.Client(api_key=os.environ["ANTHROPIC_API_KEY"])

class Person(BaseModel):
    name: str
    age: int
    email: str

# Ask Claude to produce a person as JSON
response = client.messages.create(
    model = "claude-sonnet-4-6",
    max_tokens = 1024,
    messages = [{
        "role" : "user",
        "content" : "Give me a fictional person as JSON with fields: name (string), age (integer), email (string). Return ONLY the JSON object, no other text."
    }]
)

# Pull the text out of Claude's response (same .content[0].text from before reAct loop)
raw_text = response.content[0].text
print("Claude returned: ")
print(raw_text + "\n")

'''
THE BELOW WAS REPLACED DUE TO PARSING ERROR
# Turn the JSON text into a Python dictionary
data = json.loads(raw_text)        # json.loads = "load string" → converts JSON text to a dict
'''
# Turn the JSON text into a Python dictionary: Soltion!
# Remove the ```json {}``` part and extract only content within brackets
match = re.search(r'\{[\s\S]*\}', raw_text)     # find the first {...} block
if match:
    json_text = match.group(0)      # .group(0) = pulls out the actual matched text (the clean {...} part)
    data = json.loads(json_text)    # now parse the clean JSON
else:
    print("No JSON found in Claude's response!")
    data = {}

# Now validate it with Pydantic, catching failures like before
try:
    person = Person(**data)
    print("Valid! -> ", person)

except ValidationError as e:   
    print("Validation failed!")                      
    print(e)
