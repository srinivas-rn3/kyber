from strands import Agent

FAQS = {
    "reset password": "To reset your password, open the sign-in page and click 'Forgot Password'.",
    "vpn issue": "For VPN issues, reconnect once, verify internet access, and contact IT if the tunnel still fails.",
    "email setup": "To set up email, open Outlook, sign in with your work account, and complete MFA if prompted.",
    "laptop slow": "Restart the laptop, close unused apps, and check Task Manager for high CPU or memory usage."
}

def answer_question(user_input: str) -> str:
    text = user_input.lower()

    for key, value in FAQS.items():
        if key in text:
            return value

    return "I know these topics: reset password, vpn issue, email setup, laptop slow."

agent = Agent(
    name="faq-agent",
    description="A small FAQ support agent"
)

def handler(event):
    message = ""
    if isinstance(event, dict):
        message = event.get("message") or event.get("prompt") or ""
    else:
        message = str(event)

    return {
        "response": answer_question(message)
    }