import boto3
from botocore.exceptions import ClientError      
from config import *

def send_email(recipient = None, body_text = None, body_html = None, subject = None):        
    # initializing the response 
    response = {'success': True, 'reason': None}

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    recipient if recipient else DEFAULT_RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': body_html if body_html else DEFAULT_BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': body_text if body_text else DEFAULT_BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': subject if subject else DEFAULT_SUBJECT,
                },
            },
            Source=SENDER
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        response['success'] = False
        response['reason'] = e.response['Error']['Message']
    
    return response