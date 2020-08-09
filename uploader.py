import sys, os
import configparser
import boto3
import uuid

path = os.getcwd()
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
bucket_name = config['SETTING']['BUCKET_NAME']
region = config['AWS']['REGION']

s3 = boto3.client(
    's3',
    aws_access_key_id = config['AWS']['ACCESS_KEY'],
    aws_secret_access_key = config['AWS']['SECRET_KEY']
)

def have_bucket():
    bucket_list = [bucket['Name'] for bucket in s3.list_buckets()['Buckets']] 
    if bucket_name not in bucket_list:
        print(f"Cannot find Bucket: {bucket_name}")
        return False
    return True

def create_bucket():
    location = {'LocationConstraint': region}
    s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
    print(f"Created bucket [{bucket_name}] on {region}")

def upload(filename):
    f = filename.split('/')[-1]
    extension = f.split('.')[-1]
    f = '.'.join(f.split('.')[:-1])
    f = f"{f}-{str(uuid.uuid4())[:4]}.{extension}"
    
    s3.upload_file(Filename=filename, Bucket=bucket_name, Key=f)
    s3.put_object_acl(ACL='public-read', Bucket=bucket_name, Key=f)
    url = f'https://{bucket_name}.s3.{region}.amazonaws.com/{f}'
    return url

def upload_files(files):
    files.pop(0)
    for file in files:
        if file == None:
            break
        print(upload(file))

    
if __name__ == "__main__":
    if not have_bucket():
        create_bucket()
    upload_files(sys.argv)