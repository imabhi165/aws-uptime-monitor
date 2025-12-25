import urllib.request
import boto3
from datetime import datetime

TABLE_NAME = "WebsiteUptimeLogs"
WEBSITE_URL = "https://imabhi165.github.io/Aws-Pactice-portfolio-website-test/"
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:564445391799:uptime-alerts"

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

def lambda_handler(event, context):
    table = dynamodb.Table(TABLE_NAME)
    timestamp = datetime.utcnow().isoformat()

    try:
        response = urllib.request.urlopen(WEBSITE_URL, timeout=5)
        status_code = response.getcode()
        status = "UP" if status_code == 200 else "DOWN"
    except:
        status = "DOWN"
        status_code = "ERROR"

    table.put_item(
        Item={
            "website": WEBSITE_URL,
            "timestamp": timestamp,
            "status": status,
            "status_code": str(status_code)
        }
    )

    if status == "DOWN":
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="Website Down Alert",
            Message=f"{WEBSITE_URL} is DOWN at {timestamp}"
        )

    return {
        "status": status
    }
