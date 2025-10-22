from typing import TypedDict


# Define a TypedDict
class Person(TypedDict):
    name: str
    age: int
    email: str

# Use the TypedDict
person1:Person = {
    "name":"Srinu",
    "age": 34,
    "email":"srin@dddd.com"
}
print(person1['name'])
print(person1['age'])
##################################

class UserResponse(TypedDict):
    id: int
    name: str
    email: str

def fetch_user()-> UserResponse:
    return{"id":122,"name":"Srinu","email":"srinu@dddd.com"}

print(fetch_user()['name'])