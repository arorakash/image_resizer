from flask import Flask, request, jsonify, render_template
import boto3
import uuid
import os
from config import AWS_REGION, AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_S3_INPUT_BUCKET, AWS_S3_OUTPUT_BUCKET

app = Flask(__name__)
s3_client = boto3.client('s3', 
    aws_access_key_id=AWS_ACCESS_KEY, 
    aws_secret_access_key=AWS_SECRET_KEY, 
    region_name=AWS_REGION,
    endpoint_url=f'https://s3.{AWS_REGION}.amazonaws.com',
    config=boto3.session.Config(s3={'addressing_style': 'virtual'})
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        request_id = str(uuid.uuid4())
        filename = file.filename
        s3_path = f"{request_id}/{filename}"
        
        s3_client.upload_fileobj(file, AWS_S3_INPUT_BUCKET, s3_path)
        
        return jsonify({'request_id': request_id, 'message': 'Image uploaded successfully'}), 200
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/get_resized/<request_id>', methods=['GET'])
def get_resized_image(request_id):
    response = s3_client.list_objects_v2(Bucket=AWS_S3_OUTPUT_BUCKET, Prefix=f"{request_id}/")
    
    if 'Contents' in response:
        resized_file = response['Contents'][0]['Key']
        print(f"resized_file: {resized_file}")
        presigned_url = s3_client.generate_presigned_url('get_object',
                                                         Params={'Bucket': AWS_S3_OUTPUT_BUCKET, 'Key': resized_file},
                                                         ExpiresIn=3600)
        return jsonify({'presigned_url': presigned_url}), 200
    
    return jsonify({'message': 'Image is being resized, please try after 30 seconds'}), 202

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
