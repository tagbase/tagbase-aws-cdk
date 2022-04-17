import os

import aws_cdk as cdk
import aws_cdk.assertions as assertions
import pytest as pytest
from tagbase_vpc.tagbase_vpc_stack import TagbaseVPCStack


@pytest.mark.skip(reason="AWS environment variables need to be set. See README.")
def test_tagbase_vpc_created():
    env = cdk.Environment(
        account=os.getenv("TAGBASE_AWS_ACCOUNT"), region=os.getenv("TAGBASE_DEFAULT_REGION")
    )
    app = cdk.App()
    stack = TagbaseVPCStack(app, "tagbase-vpc-stack", env=env)
    template = assertions.Template.from_stack(stack)
    template.has_resource_properties("AWS::EC2::VPC", {"VisibilityTimeout": 300})
