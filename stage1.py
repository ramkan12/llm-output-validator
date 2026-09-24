# Stage 1: Define the Pydantic Model

from pydantic import BaseModel      # what you inherit from to define a shape

# Define the exact shape you expect the data to have.
# Each line says: field name, its type. Pydantic will ENFORCE these.
class Person(BaseModel):
    name: str
    age: int
    email: str

# Try it on Good data first (a normal Python dictionary) 
# integers can also be passed as strings e.g. '21')
good_data = {"name" : "Riham", "age" : 21, "email" : "khanriham38@gmail.com"}

person = Person(**good_data)        # **good_data unpacks the dict into name=..., age=..., email=...
print("Valid!")
print(person)
print(person.name)      # you can access fields directly once validated