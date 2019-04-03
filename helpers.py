import os
import boto3, botocore
from config import Config
from models.user import User
from flask_login import current_user

s3 = boto3.client(
   "s3",
   aws_access_key_id=Config.S3_KEY,
   aws_secret_access_key=Config.S3_SECRET
)

def upload_file_to_s3(file, bucket_name, acl="public-read"):
    user = User.get_by_id(current_user.id)
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            str(user.id) + '/' + file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e

    return f"{Config.S3_LOCATION}{file.filename}"

def allowed_file(filename):
    allowed_extensions = set(['png', 'jpeg', 'jpg', 'gif'])
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extensions
