import boto3
from datetime import datetime
import uuid

dynamodb = boto3.resource("dynamodb", region_name="ap-south-1")
table = dynamodb.Table("UserFeedback")

def show_summary(state):
    print("\n✅ Thanks for your time! Here’s what you shared:")

    feedbacks = state.get("feedbacks", [])

    if not feedbacks:
        print("No feedbacks shared yet.")
    else:
        for i, fb in enumerate(feedbacks, start=1):
            print(f"{i}. {fb}")

        # 🧾 Save to DynamoDB
        try:
            session_id = f"sess-{uuid.uuid4().hex[:8]}"
            table.put_item(
                Item={
                    "session_id": session_id,
                    "timestamp": datetime.utcnow().isoformat(),
                    "feedbacks": feedbacks,
                }
            )
            print(f"🗄️ Saved feedback to DynamoDB (session: {session_id}) ✅")
        except Exception as e:
            print(f"⚠️ Failed to save to DynamoDB: {e}")

    print("🙏 Goodbye!")
    return state
