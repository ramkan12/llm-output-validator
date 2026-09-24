# Stage 2: Feed it Deliberately Broken Data

from pydantic import BaseModel      

class Person(BaseModel):
    name: str
    age: int
    email: str

# feed bad data, in this case: missing age field
bad_data = {"name" : "Riham", "email" : "khanriham38@gmail.com"}

person = Person(**bad_data)        
print("Valid!")
print(person)
print(person.name)      

'''
ram_kan@mac Validate+Retry % python stage2.py
Traceback (most recent call last):
  File "/Users/ram_kan/Desktop/AgenticAIRoadMap/Validate+Retry/stage2.py", line 11, in <module>
    person = Person(**bad_data)
  File "/opt/homebrew/lib/python3.13/site-packages/pydantic/main.py", line 250, in __init__
    validated_self = self.__pydantic_validator__.validate_python(data, self_instance=self)
pydantic_core._pydantic_core.ValidationError: 1 validation error for Person
age
  Field required [type=missing, input_value={'name': 'Riham', 'email'...'khanriham38@gmail.com'}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.12/v/missing

'''