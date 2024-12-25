import json
import boto3
from datetime import datetime

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('passcodes')  

def lambda_handler(event, context):
    # Validate and parse the event body
    try:
        if isinstance(event.get('body'), dict):
            body = event['body']
        elif isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            raise ValueError("Invalid body format")
    except (ValueError, json.JSONDecodeError) as e:
        return {
            "statusCode": 400,
            "body": json.dumps("Invalid request body format. Ensure JSON format.")
        }

    # Extract OTP and passcodeID
    otp = body.get("otp")
    passcode_id = body.get("passcodeID")

    # Check if both OTP and passcodeID are provided
    if not otp or not passcode_id:
        return {
            "statusCode": 400,
            "body": json.dumps("Missing required fields: 'otp' and 'passcodeID'.")
        }

    # Retrieve stored OTP and expiration time from DynamoDB
    try:
        response = table.get_item(Key={'passcodeID': passcode_id})
        if 'Item' not in response:
            return {
                "statusCode": 404,
                "body": json.dumps("Record not found for the provided passcodeID.")
            }
        
        stored_otp = response['Item'].get('otp')
        expiration = response['Item'].get('expiration')
        
        # Validate OTP and check if it is still valid
        current_time = int(datetime.utcnow().timestamp())
        if otp == stored_otp and current_time < expiration:
            return {
                "statusCode": 200,
                "body": json.dumps("OTP validated successfully. Access granted.")
            }
        else:
            return {
                "statusCode": 403,
                "body": json.dumps("Invalid or expired OTP. Access denied.")
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error processing record: {str(e)}")
        }
