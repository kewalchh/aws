import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ProductCatalog')

def lambda_handler(event, context):
    # TODO implement
    
    prodId = event['prodId']
    response = table.get_item(Key={'Id':prodId})
    return response['Item']
