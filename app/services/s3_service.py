import boto3
import botocore

from app.utils.constants import REGION, WRITE_BUCKET


class S3Service(object):
    def __init__(self):
        self.s3_resource = boto3.resource('s3', region_name=REGION)
        self.s3_client = boto3.client('s3', region_name=REGION)

    def get_file_to_write(self, request_id, body):
        try:
            original_file = self.s3_resource.Object(body['bucket_name'], body['file_name'])
            original_file.load()
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                print('{}| file {} doesnt exist in a bucket {}'.format(request_id, body['file_name'], body['bucket_name']))
            else:
                print('{}| Error file {}  {}'.format(request_id, body['file_name'], str(e)))
                raise SystemExit
        else:
            try:
                write_file = self.s3_resource.Object(WRITE_BUCKET, body['file_name'])
                write_file.load()
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == '404':
                    print('{}| file {} doesnt exist in a bucket {}'.format(request_id, body['file_name'], WRITE_BUCKET))
                    return original_file
                else:
                    print('{}| Error file {}  {}'.format(request_id, body['file_name'], str(e)))
            else:
                return write_file

    def save_file(self, request_id, body, data):
        try:
            self.s3_client.put_object(Body=''.join(data), Bucket=WRITE_BUCKET, Key=body['file_name'])
        except Exception as e:
            print('{}| Error save file {}  {}'.format(request_id, body['file_name'], str(e)))
            raise
