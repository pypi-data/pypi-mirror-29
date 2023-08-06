import boto3
from botocore.exceptions import ClientError

ARN_PREFIX = 'arn:aws:s3:::'

client = boto3.client('s3')


def arn_from_bucket_name(bucket_name: str) -> str:
    return ARN_PREFIX + bucket_name


def bucket_name_from_arn(bucket_arn: str) -> str:
    if not ARN_PREFIX in bucket_arn:
        raise ValueError(bucket_arn + ' is not a valid ARN')
    return bucket_arn[len(ARN_PREFIX):]


def empty_bucket(*, bucket_name: str = "", bucket_arn: str = "") -> None:
    if not bucket_name and not bucket_arn:
        raise ValueError("either bucket_name or bucket_arn must be provided")
    bucket_name = bucket_name if bucket_name else bucket_name_from_arn(
        bucket_arn)
    bucket = boto3.resource('s3').Bucket(bucket_name)
    bucket.objects.all().delete()


def object_exists(bucket: str, key: str) -> bool:
    try:
        client.head_object(Bucket=bucket, Key=key)
    except ClientError as error:
        error_message = error.response['Error']['Message']
        if error_message == "Not Found" or error_message == "The specified bucket does not exist":
            return False
        else:
            raise
    else:
        return True
