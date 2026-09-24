# Stage 3: Catch the Error Cleanly

from pydantic import BaseModel, ValidationError     # new library!!   

class Person(BaseModel):
    name: str
    age: int
    email: str

# missed age field on purpose 
bad_data = {"name" : "Riham", "email" : "khanriham38@gmail.com"}

try:
    person = Person(**bad_data)         # try to Validate
    print("Valid!")
    print(person)
except ValidationError as e:            # if validation fails, catch it inside e instead of crashing    
    print("Validation falied!")
    print(e)                            # print the detailed error (what we'll send back the LLM later next stage)
