import aws_cdk as cdk

from lake_formation_practice import LakeFormationPracticeStack


app = cdk.App()
environment = app.node.try_get_context("environment")
LakeFormationPracticeStack(
    app,
    "LakeFormationPracticeStack",
    env=cdk.Environment(region=environment["AWS_REGION"]),
    environment=environment,
)
app.synth()
