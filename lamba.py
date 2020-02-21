import json
from pr_data import get_entities_from_webhook_data
from lumberjack import lumberjack
import boto3
import os
import base64
from botocore.exceptions import ClientError

def get_secret():
    secret_name = "GITHUB_WEBHOOK_SECRET"
    region_name = "ap-south-1"
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            raise e
    else:
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            print("secret")
            print(secret)
            return secret
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            print("decoded_binary_secret")
            print(decoded_binary_secret)
            return decoded_binary_secret




def get_env(key):
    kms = boto3.client('kms')
    val = os.environ[key]
    val = kms.decrypt(CiphertextBlob=base64.b64decode(val))['Plaintext']
    print(val)
    return val.decode("utf-8")
    
    
def lambda_handler(event, context):
    
    print(event)
    return lumberjack()
