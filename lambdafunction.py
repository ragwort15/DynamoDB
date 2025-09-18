import json
import boto3 # type: ignore
from boto3.dynamodb.conditions import Key # pyright: ignore[reportMissingImports]


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('StudentRecords')

def lambda_handler(event, context):
    http_method = event['httpMethod']

    
    if http_method == 'POST':
        student = json.loads(event['body'])
        table.put_item(Item=student)
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Student record added successfully'})
        }

    
    elif http_method == 'GET':
        student_id = event['queryStringParameters']['student_id']
        response = table.get_item(Key={'student_id': student_id})

        if 'Item' in response:
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(response['Item'])
            }
        else:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Student not found'})
            }

    
    elif http_method == 'PUT':
        student = json.loads(event['body'])
        student_id = student['student_id']

        
        response = table.update_item(
            Key={'student_id': student_id},
            UpdateExpression="set #n=:n, course=:c",
            ExpressionAttributeNames={'#n': 'name'},
            ExpressionAttributeValues={
                ':n': student['name'],
                ':c': student['course']
            },
            ReturnValues="UPDATED_NEW"
        )

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'message': 'Student record updated', 'updated': response['Attributes']})
        }

    