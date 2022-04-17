import os

import aws_cdk as cdk
import aws_cdk.assertions as assertions
import pytest as pytest
from tagbase_db.tagbase_db_stack import TagbaseDBStack


@pytest.mark.skip(reason="AWS environment variables need to be set. See README.")
def test_tagbase_db_postgres_created():
    env = cdk.Environment(
        account=os.getenv("TAGBASE_AWS_ACCOUNT"),
        region=os.getenv("TAGBASE_DEFAULT_REGION"),
    )
    app = cdk.App()
    stack = TagbaseDBStack(app, "tagbase-db-stack", env=env, new_vpc=None)
    template = assertions.Template.from_stack(stack)
    template.has_resource_properties("AWS::RDS::DBInstance", {"VisibilityTimeout": 300})
