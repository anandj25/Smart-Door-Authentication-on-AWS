# Smart Door Authentication System

The Smart Door Authentication System is a secure and intelligent solution that uses AWS services to authenticate visitors, manage access, and enhance security. The system leverages video analysis, facial recognition, and OTP-based authentication to provide a seamless and user-friendly experience.

---

## 📝 Overview

The system aims to:
- Process video streams to identify faces.
- Authenticate known visitors via OTP for access.
- Notify system owners about unknown visitors and manage their access.
- Provide a virtual door interface for OTP-based access.

---

## 🏗️ Architecture

The system comprises three main components:
1. **Visitor Vault**:
   - Stores visitor details and photos in DynamoDB and S3.
2. **Stream Analysis**:
   - Uses Kinesis Video Streams and Amazon Rekognition for real-time video analysis.
3. **Access Authorization**:
   - Provides web interfaces for approving visitors and validating OTPs.

---

## 🚀 Implementation Steps

### 1. Visitor Vault
- **S3 Bucket**:
  - Store visitor photos in an S3 bucket.
- **DynamoDB Tables**:
  - **Passcodes Table (DB1)**:
    - Schema: `{"visitorId": STRING, "passcode": STRING, "TTL": NUMBER}`
    - Automatically expires records after 5 minutes.
  - **Visitors Table (DB2)**:
    - Stores visitor details (`faceId`, `name`, `phoneNumber`, `photos`).
    - Index by `FaceId` for efficient lookups.

### 2. Stream Analysis
- **Kinesis Video Stream**:
  - Captures video input from an IP camera or simulated source.
- **Amazon Rekognition**:
  - Analyzes video streams to detect faces.
  - Outputs analysis results to a Kinesis Data Stream (KDS1).
  - Triggers a Lambda function for each event.
- **Notifications**:
  - **Known Faces**:
    - Sends SMS with a one-time passcode (OTP).
    - Stores OTP in DB1 with a 5-minute expiration.
  - **Unknown Faces**:
    - Sends SMS with a photo of the visitor and an approval link.

### 3. Access Authorization
- **Web Page 1: Visitor Approval**:
  - Allows system owners to approve unknown visitors.
  - Captures visitor details and generates OTPs for approved visitors.
- **Web Page 2: Virtual Door**:
  - Validates OTPs against DB1.
  - Displays access status (success or permission denied).

---

## ✅ Acceptance Criteria
- Notify system owners about unknown visitors with images and approval links.
- Generate and send unique OTPs valid for 5 minutes.
- Automatically authenticate returning visitors with new OTPs.
- Allow visitors to access the virtual door using OTPs.

---

## 🛠️ Tools and Resources

### AWS Services:
- **Kinesis Video Streams**: Captures and streams video input.
- **Amazon Rekognition**: Performs facial recognition.
- **DynamoDB**: Stores visitor and OTP data.
- **S3**: Stores visitor photos.
- **Lambda**: Handles backend logic.
- **SNS**: Sends notifications via SMS.

### SDKs:
- **Kinesis Video Streams Producer SDK**
- **AWS SDK for APIs**

### Web Development:
- HTML, CSS, JavaScript
- REST API integration

---

## 📋 Requirements

### AWS Configuration:
- Configure required AWS services:
  - **Kinesis Video Streams** with Rekognition integration.
  - **DynamoDB** with TTL enabled for OTP expiration.
  - **S3** for photo storage.
- Ensure appropriate IAM permissions for all services.

### Code Deployment:
- Use AWS Lambda for backend logic.
- Host web pages on AWS S3 or a web hosting service.

### Testing:
- Simulate video streams for Rekognition analysis.
- Test OTP workflows for known and unknown visitors.

### Dependencies:
- Python 3.x for Lambda functions
- Required AWS SDKs and libraries
- Kinesis Video Streams Producer SDK

---

## 📖 Setup Instructions

1. **Visitor Vault**:
   - Create an S3 bucket to store visitor photos.
   - Set up DynamoDB tables (`DB1` for passcodes, `DB2` for visitor details).

2. **Stream Analysis**:
   - Configure a Kinesis Video Stream to capture video input.
   - Integrate Rekognition Video for real-time analysis.
   - Set up a Lambda function to handle Rekognition events and notifications.

3. **Access Authorization**:
   - Develop two web pages:
     - **Visitor Approval Page** for approving unknown visitors.
     - **Virtual Door Page** for OTP validation and visitor access.

4. **Testing**:
   - Simulate video streams for testing Rekognition analysis.
   - Validate OTP generation, expiration, and usage workflows.

---

This repository contains all the required code and instructions to deploy and test the Smart Door Authentication System. For any queries or support, please reach out to the project maintainers.
