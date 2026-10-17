
import json
import os
import uuid
import logging

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sfn = boto3.client("stepfunctions")
STATE_MACHINE_ARN = os.environ["STATE_MACHINE_ARN"]


def response(status, body):
    return {
        "statusCode": status,
        "headers": {"content-type": "application/json"},
        "body": json.dumps(body)
    }


def lambda_handler(event, context):
    try:
        body = event.get("body")

        if isinstance(body, str):
            payload = json.loads(body)
        elif isinstance(body, dict):
            payload = body
        else:
            return response(400, {
                "error": "Request body must be JSON."
            })

        employee = payload.get("EmployeeId")
        item = payload.get("PurchaseItem")
        amount = payload.get("PurchaseAmount")

        if not isinstance(employee, str) or not employee.strip():
            return response(400, {
                "error": "EmployeeId is required."
            })

        if not isinstance(item, str) or not item.strip():
            return response(400, {
                "error": "PurchaseItem is required."
            })

        if (isinstance(amount, bool)
                or not isinstance(amount, (int, float))
                or amount <= 0
                or amount == float("inf")
                or amount == float("-inf")
                or amount != amount):
            return response(400, {
                "error": "PurchaseAmount must be a positive number."
            })

        request_id = str(uuid.uuid4())

        workflow_input = {
            "RequestId": request_id,
            "EmployeeId": employee.strip(),
            "PurchaseAmount": amount,
            "PurchaseItem": item.strip()
        }

        result = sfn.start_execution(
            stateMachineArn=STATE_MACHINE_ARN,
            input=json.dumps(workflow_input)
        )

        return response(202, {
            "message": "Purchase request accepted.",
            "requestId": request_id,
            "executionArn": result["executionArn"]
        })

    except json.JSONDecodeError:
        return response(400, {
            "error": "Invalid JSON format."
        })

    except ClientError:
        logger.exception("AWS service error")
        return response(500, {
            "error": "Could not start the workflow."
        })

    except Exception:
        logger.exception("Unexpected error")
        return response(500, {
            "error": "Internal server error."
        })
