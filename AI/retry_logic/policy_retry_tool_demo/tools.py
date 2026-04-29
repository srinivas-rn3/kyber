from langchain_core.tools import tool
@tool
def check_expiry(days:int,max_allowed:int):
    """Returns True if policy is expired beyond allowed days."""
    return days > max_allowed

@tool
def check_amount(amount:int,max_allowed:int):
    """Returns True if due amount is above allowed."""
    return amount > max_allowed
