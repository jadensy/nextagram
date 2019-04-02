import os
import boto3, botocore
from config import Config
from app import app

s3 = boto3.client(
   "s3",
   aws_access_key_id=Config.S3_KEY,
   aws_secret_access_key=Config.S3_SECRET
)

def upload_file_to_s3(file, bucket_name, acl="public-read"):
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e

    return f"{app.config.Config.S3_LOCATION}{file.filename}"


def allowed_file(filename):
    allowed_extensions = set(['png', 'jpeg', 'jpg', 'gif'])
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extensions
