import json
import boto3
import random
import uuid
from datetime import datetime, timedelta
import base64

# Initialize clients
ses_client = boto3.client('ses')
dynamodb_client = boto3.resource('dynamodb')
table_passcodes = dynamodb_client.Table('passcodes')  # DynamoDB table for OTPs
table_visitors = dynamodb_client.Table('visitors')  # DynamoDB table for visitors

SENDER_EMAIL = ""  # SES verified sender email
VISITOR_EMAIL = ""  # Visitor email for OTP
OWNER_PHONE_NUMBER = ""  # Phone number for alerts about unknown faces

def generate_otp():
    """Generates a 6-digit OTP."""
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    """Send OTP to visitor's email via SES."""
    try:
        message_body = f"Your OTP to access the virtual door is {otp}. This code will expire in 5 minutes."
        ses_client.send_email(
            Source=SENDER_EMAIL,
            Destination={'ToAddresses': [email]},
            Message={
                'Subject': {'Data': 'Your OTP for Access'},
                'Body': {'Text': {'Data': message_body}}
            }
        )
        print(f"OTP {otp} sent to {email}.")
    except Exception as e:
        print(f"Failed to send OTP to {email}: {e}")

def store_otp(email, otp):
    """Store OTP in DynamoDB with expiration time."""
    expiration = int((datetime.utcnow() + timedelta(minutes=5)).timestamp())
    passcode_id = str(uuid.uuid4())
    table_passcodes.put_item(
        Item={
            'passcodeID': passcode_id,
            'email': email,
            'otp': otp,
            'expiration': expiration
        }
    )
    print(f"Stored OTP {otp} for {email} in DynamoDB with passcodeID {passcode_id}.")

def handle_known_face():
    """Handle the processing and notification for a known face."""
    otp = generate_otp()
    send_otp_email(VISITOR_EMAIL, otp)
    store_otp(VISITOR_EMAIL, otp)

def handle_unknown_face(face_id, image_url):
    """Handle notification for an unknown face."""
    # Send email notification to the owner for unknown face detection
    try:
        message_body = f"An unknown visitor was detected. Review the image here: {image_url}"
        ses_client.send_email(
            Source=SENDER_EMAIL,
            Destination={'ToAddresses': [SENDER_EMAIL]},
            Message={
                'Subject': {'Data': 'Unknown Visitor Detected'},
                'Body': {'Text': {'Data': message_body}}
            }
        )
        print(f"Notification for unknown visitor sent to {SENDER_EMAIL}.")
    except Exception as e:
        print(f"Failed to notify owner for unknown visitor: {e}")

def handler(event, context):
    for record in event['Records']:
        try:
            # Decode base64 data to a JSON string
            decoded_data = base64.b64decode(record['kinesis']['data']).decode('utf-8')
            payload = json.loads(decoded_data)
            print("Decoded payload:", payload)

            # Timestamp for debugging real-time frame processing
            timestamp = record.get('kinesis', {}).get('approximateArrivalTimestamp', 'Unknown')
            print(f"Processing frame at timestamp: {timestamp}")

            # Process the payload for face recognition results
            if 'FaceSearchResponse' in payload:
                for face_response in payload['FaceSearchResponse']:
                    if 'MatchedFaces' in face_response and face_response['MatchedFaces']:
                        handle_known_face()
                    elif 'MatchedFaces' in face_response and not face_response['MatchedFaces']:
                        face_id = str(uuid.uuid4())  # Simulating unique face ID for unknown face
                        image_url = "https://example.com/path-to-image.jpg"  # Replace with actual image URL if available
                        handle_unknown_face(face_id, image_url)
                    else:
                        print("No faces detected in this frame.")

        except json.JSONDecodeError:
            print("Error: Failed to decode JSON payload.")
            print("Raw Kinesis data:", record['kinesis']['data'])
        except Exception as e:
            print(f"Error processing record: {e}")

    return {
        "statusCode": 200,
        "body": json.dumps("Processed records and sent OTP if face was matched")
    }
