from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_lambda as _lambda,
    aws_s3 as s3,
    triggers,
)
from constructs import Construct


class LakeFormationPracticeStack(Stack):

    def __init__(
        self, scope: Construct, construct_id: str, environment: dict, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.s3_bucket = s3.Bucket(
            self,
            "S3Bucket",
            bucket_name=environment["S3_BUCKET"],
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        self.upload_file_to_lakehouse_lambda = _lambda.Function(
            self,
            "UploadFileToLakehouseLambda",
            function_name="upload-file-to-lakehouse",  # hard coded
            handler="handler.lambda_handler",
            memory_size=128,
            timeout=Duration.seconds(3),  # should be instantaneous
            runtime=_lambda.Runtime.PYTHON_3_10,
            environment={
                "S3_BUCKET": environment["S3_BUCKET"],
            },
            code=_lambda.Code.from_asset(
                "lambda/upload_file_to_lakehouse",
                exclude=[".venv/*"],
            ),
        )


        # connect the AWS resources
        self.trigger_upload_file_to_lakehouse_lambda = triggers.Trigger(
            self,
            "TriggerUploadFileToLakehouseLambda",
            handler=self.upload_file_to_lakehouse_lambda,  # this is underlying Lambda
            execute_after=[self.s3_bucket],
            # execute_before=[],
            # invocation_type=triggers.InvocationType.REQUEST_RESPONSE,
        )
        self.s3_bucket.grant_write(self.upload_file_to_lakehouse_lambda)