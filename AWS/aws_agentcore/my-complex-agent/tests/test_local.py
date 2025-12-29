"""
Local Testing Script
Test your agent locally before deploying to AWS
"""
import requests
import json

# Local agent URL (when running agent.py)
LOCAL_URL = "http://localhost:8080/invocations"

def test_agent(prompt, user_id="test_user", session_id="test_session"):
    """Send test request to local agent"""
    payload = {
        "prompt": prompt,
        "user_id": user_id,
        "session_id": session_id
    }
    
    print(f"\n{'='*60}")
    print(f"USER: {prompt}")
    print(f"{'='*60}")
    
    try:
        response = requests.post(
            LOCAL_URL,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        result = response.json()
        print(f"AGENT: {result.get('response', 'No response')}")
        
        if result.get('status') == 'error':
            print(f"ERROR: {result.get('error')}")
            
    except Exception as e:
        print(f"Connection error: {e}")
        print("Make sure agent.py is running (python agent.py)")

if __name__ == "__main__":
    print("Starting local agent tests...")
    print("Make sure you have 'python agent.py' running in another terminal")
    
    # Test 1: Order status check
    test_agent("Can you check the status of order ORD-12345?")
    
    # Test 2: Account information
    test_agent("What are the details for customer CUST-001?")
    
    # Test 3: FAQ search
    test_agent("What is your return policy?")
    
    # Test 4: General conversation
    test_agent("What can you help me with?")
    
    # Test 5: Shipping information
    test_agent("Tell me about shipping options")
    
    print("\n" + "="*60)
    print("Testing complete!")
