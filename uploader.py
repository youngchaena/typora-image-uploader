import configparser
import boto3

def create_bucket(client, bucket_name, region):
    location = {'LocationConstraint': region}
    client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
    # client.put_bucket_acl(Bucket=bucket_name, ACL="public-read")
    print(f"Created bucket [{bucket_name}] on {region}")
    

config = configparser.ConfigParser()
config.read('config.ini')
bucket_name = config['SETTING']['BUCKET_NAME']
region = config['AWS']['REGION']

s3 = boto3.client(
    's3',
    aws_access_key_id = config['AWS']['ACCESS_KEY'],
    aws_secret_access_key = config['AWS']['SECRET_KEY']
)
print("Connection success to AWS S3")

bucket_list = [bucket['Name'] for bucket in s3.list_buckets()['Buckets']] 
# print(bucket_list)

if config['SETTING']['BUCKET_NAME'] not in bucket_list:
    print(f"Cannot find Bucket: {bucket_name}")
    create_bucket(s3, bucket_name, region)

# image = open('python_logo.png', 'rb')
filename = 'python_logo.png'
s3.upload_file(filename, bucket_name, filename)
s3.put_object_acl(ACL='public-read', Bucket=bucket_name, Key=filename)
url = f'https://{bucket_name}.s3.{region}.amazonaws.com/{filename}'
print(f"Uploaded {filename}")
print(f"url : {url}")
