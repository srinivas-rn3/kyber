from bedrock_agentcore import BedrockAgentCoreApp

app = BedrockAgentCoreApp()

FAQS = {
    "reset password": "To reset your password, open the sign-in page and click 'Forgot Password'.",
    "vpn issue": "For VPN issues, reconnect once, verify internet access, and contact IT if the tunnel still fails.",
    "email setup": "To set up email, open Outlook, sign in with your work account, and complete MFA if prompted.",
    "laptop slow": "Restart the laptop, close unused apps, and check Task Manager for high CPU or memory usage."
}

@app.entrypoint
async def handler(request):
    prompt = (request.get("prompt") or request.get("message") or "").lower()

    if not prompt:
        return {"response": "Please send a prompt."}

    for key, value in FAQS.items():
        if key in prompt:
            return {"response": value}

    return {
        "response": "I know these topics: reset password, vpn issue, email setup, laptop slow."
    }

app.run()