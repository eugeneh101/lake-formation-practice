import os

import boto3


S3_BUCKET = os.environ["S3_BUCKET"]
S3_RESOURCE = boto3.resource("s3")


def lambda_handler(event, context) -> None:
    print(event)
    # create folders
    S3_RESOURCE.Object(bucket_name=S3_BUCKET, key="bronze/").put()  # hard coded
    S3_RESOURCE.Object(bucket_name=S3_BUCKET, key="silver/").put()  # hard coded
    S3_RESOURCE.Object(bucket_name=S3_BUCKET, key="gold/").put()  # hard coded

    # upload data
    S3_RESOURCE.Object(  # hard coded
        bucket_name=S3_BUCKET, key="bronze/mock_data.csv"  # hard coded
    ).upload_file(
        Filename="mock_data.csv"  # hard coded
    )
