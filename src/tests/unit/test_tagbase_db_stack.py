import aws_cdk as core
import aws_cdk.assertions as assertions

from tagbase_db.tagbase_db_stack import TagbaseDBStack


def test_tagbase_db_postgres_created():
    app = core.App()
    stack = TagbaseDBStack(app, "tagbase-db-stack")
    template = assertions.Template.from_stack(stack)
    template.has_resource_properties("AWS::RDS::DBInstance", {
        "VisibilityTimeout": 300
    })
