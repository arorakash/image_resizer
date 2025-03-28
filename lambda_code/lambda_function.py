import json
import boto3
import os
from PIL import Image
from io import BytesIO

s3_client = boto3.client('s3')
OUTPUT_BUCKET = os.environ['OUTPUT_BUCKET']

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        request_id = key.split('/')[0]
        file_name = key.split('/')[1]
        output_key = f"{request_id}/{file_name}"

        response = s3_client.get_object(Bucket=bucket, Key=key)
        image_data = response['Body'].read()
        
        image = Image.open(BytesIO(image_data))
        width, height = image.size
        
        max_size = 256
        if max(width, height) > max_size:
            image.thumbnail((max_size, max_size))
        
        buffer = BytesIO()
        image.save(buffer, format=image.format)
        buffer.seek(0)
        
        s3_client.put_object(Bucket=OUTPUT_BUCKET, Key=output_key, Body=buffer)
        
    return {
        'statusCode': 200,
        'body': json.dumps('Image resized successfully!')
    }
