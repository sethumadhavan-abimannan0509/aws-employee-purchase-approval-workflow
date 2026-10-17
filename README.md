# AWS Employee Purchase Approval Workflow

## Project Overview

This project demonstrates a serverless employee purchase approval
workflow built using Amazon Web Services (AWS).

It processes employee purchase requests, evaluates the purchase
amount, stores the processing result in Amazon S3, and sends
status notifications using Amazon SNS.

## AWS Services Used

- Amazon API Gateway — receives purchase requests through an API.
- AWS Lambda — executes Python code to submit and process requests.
- AWS Step Functions — coordinates the workflow.
- Amazon S3 — stores purchase request records as JSON files.
- Amazon SNS — sends email notifications.
- Amazon CloudWatch — supports logging and monitoring.

## Purchase Approval Rules

The workflow evaluates requests according to these rules:

| Purchase Amount | Status |
|---|---|
| €100 or less | APPROVED |
| Above €100 and up to €500 | NEEDS_REVIEW |
| Above €500 | REJECTED |

## Workflow

1. An employee submits a purchase request through API Gateway.
2. The SubmitPurchase Lambda function validates the request
   and starts the Step Functions workflow.
3. Step Functions coordinates the processing.
4. The ProcessPurchase Lambda function evaluates the request.
5. The processing result is saved as a JSON object in Amazon S3.
6. Amazon SNS sends an email notification through the workflow.
7. Amazon CloudWatch provides logs and monitoring.

## Python Source Code

The `src` directory contains the Python Lambda function code.

## Project Status

Completed as a practical AWS learning project.

## Demonstration Video

Video link will be added here.

## Author

Sethumadhavan Abimannan
