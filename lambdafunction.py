import json
import boto3
from boto3.dynamodb.conditions import Key

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
StudentRecords = dynamodb.StudentRecords('StudentRecords')

def lambda_handler(event, context):
    http_method = event['httpMethod']

   
    if http_method == 'POST':
        student = json.loads(event['body'])
        StudentRecords.put_item(Item=student)
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Student added'})
        }

   
    elif http_method == 'GET':
        student_id = event['queryStringParameters']['student_id']
        response = StudentRecords.get_item(Key={'student_id': student_id})

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

        # Example: Update name and course (you can extend as needed)
        response = StudentRecords.update_item(
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

    
    elif http_method == 'DELETE':
        student_id = event['queryStringParameters']['student_id']
        StudentRecords.delete_item(Key={'student_id': student_id})
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'message': 'Student record deleted'})
        }

    else:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Unsupported HTTP method'})
        }
