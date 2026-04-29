from typing import TypedDict

class Policy(TypedDict):
    policy_id: str
    expiry_days: int
    policy_type: str

policy = {
    "policy_id":"deee11",
    "expiry_days":30,
    "policy_type":"car"
}
def check(policy:Policy) -> bool:
   print(policy["policy_id"])
   return policy['expiry_days'] <= 45


result = check(policy)
print(result)