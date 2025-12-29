"""
Customer Support Tools
Contains business logic functions that the agent can call
"""
from strands import tool
import logging

logger = logging.getLogger(__name__)

@tool
def check_order_status(order_id: str) -> str:
    """
    Check the status of a customer order.
    
    Args:
        order_id: The order ID to check (e.g., "ORD-12345")
    
    Returns:
        Order status information as a string
    """
    logger.info(f"Checking status for order: {order_id}")
    
    # Simulate database lookup
    # In production, this would query your order management system
    mock_orders = {
        "ORD-12345": {
            "status": "Shipped",
            "tracking": "TRK-999888",
            "estimated_delivery": "Dec 28, 2025",
            "items": "2 items"
        },
        "ORD-67890": {
            "status": "Processing",
            "tracking": None,
            "estimated_delivery": "Dec 30, 2025",
            "items": "1 item"
        }
    }
    
    order = mock_orders.get(order_id)
    
    if order:
        response = f"Order {order_id}:\n"
        response += f"- Status: {order['status']}\n"
        response += f"- Items: {order['items']}\n"
        if order['tracking']:
            response += f"- Tracking Number: {order['tracking']}\n"
        response += f"- Estimated Delivery: {order['estimated_delivery']}"
        return response
    else:
        return f"Order {order_id} not found. Please verify the order ID."

@tool
def get_account_info(customer_id: str) -> str:
    """
    Retrieve customer account information.
    
    Args:
        customer_id: Customer ID (e.g., "CUST-001")
    
    Returns:
        Account information as a string
    """
    logger.info(f"Fetching account info for: {customer_id}")
    
    # Simulate database lookup
    # In production, this would query your CRM system
    mock_accounts = {
        "CUST-001": {
            "name": "Rajesh Kumar",
            "email": "rajesh.k@example.com",
            "membership": "Gold",
            "points": 2500,
            "orders_count": 12
        },
        "CUST-002": {
            "name": "Priya Singh",
            "email": "priya.s@example.com",
            "membership": "Silver",
            "points": 800,
            "orders_count": 5
        }
    }
    
    account = mock_accounts.get(customer_id)
    
    if account:
        response = f"Account Details for {account['name']}:\n"
        response += f"- Email: {account['email']}\n"
        response += f"- Membership: {account['membership']}\n"
        response += f"- Loyalty Points: {account['points']}\n"
        response += f"- Total Orders: {account['orders_count']}"
        return response
    else:
        return f"Customer {customer_id} not found."

@tool
def search_faq(query: str) -> str:
    """
    Search the FAQ knowledge base for answers.
    
    Args:
        query: Search query or topic (e.g., "return policy", "shipping")
    
    Returns:
        Relevant FAQ answer as a string
    """
    logger.info(f"Searching FAQ for: {query}")
    
    # Simulate knowledge base search
    # In production, this could use RAG, vector database, or search API
    faq_database = {
        "return": "Return Policy: Items can be returned within 30 days of delivery. Products must be unused and in original packaging. Refunds are processed within 5-7 business days.",
        "shipping": "Shipping Information: Standard shipping takes 3-5 business days. Express shipping (1-2 days) is available for additional cost. Free shipping on orders above ₹999.",
        "payment": "Payment Methods: We accept Credit/Debit cards, UPI, Net Banking, and Cash on Delivery (COD). All transactions are secure and encrypted.",
        "warranty": "Warranty: Products come with manufacturer's warranty. Duration varies by product (check product page). Extended warranty is available at checkout.",
        "cancel": "Order Cancellation: Orders can be cancelled within 24 hours of placement. If already shipped, you can return the item after delivery."
    }
    
    # Simple keyword matching
    query_lower = query.lower()
    for keyword, answer in faq_database.items():
        if keyword in query_lower:
            return answer
    
    return "I couldn't find specific information about that. Please contact our support team at support@example.com or call 1800-123-4567 for personalized assistance."
