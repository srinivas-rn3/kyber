# memory.py
import boto3
from datetime import datetime
from config import DYNAMODB_TABLE, AWS_REGION

class SimpleMemory:
    def __init__(self, session_id):
        self.session_id = session_id
        self.dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
        self.table = self.dynamodb.Table(DYNAMODB_TABLE)
        self._ensure_table_exists()
    
    def _ensure_table_exists(self):
        try:
            self.table.table_status
        except:
            table = self.dynamodb.create_table(
                TableName=DYNAMODB_TABLE,
                KeySchema=[
                    {'AttributeName': 'session_id', 'KeyType': 'HASH'},
                    {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'session_id', 'AttributeType': 'S'},
                    {'AttributeName': 'timestamp', 'AttributeType': 'S'}
                ],
                BillingMode='PAY_PER_REQUEST'
            )
            table.wait_until_exists()
            self.table = table
    
    def save_conversation(self, question, answer, sources=None):
        item = {
            'session_id': self.session_id,
            'timestamp': datetime.now().isoformat(),
            'question': question,
            'answer': answer,
            'sources': sources or []
        }
        self.table.put_item(Item=item)
    
    def get_history(self, limit=10):
        """Get conversation history in chronological order (oldest first)"""
        response = self.table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('session_id').eq(self.session_id),
            ScanIndexForward=True,  # True = oldest first (chronological)
            Limit=limit
        )
        return response.get('Items', [])