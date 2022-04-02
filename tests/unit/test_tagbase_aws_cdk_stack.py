import aws_cdk as core
import aws_cdk.assertions as assertions

from tagbase_aws_cdk.tagbase_aws_cdk_stack import TagbaseAwsCdkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in tagbase_aws_cdk/tagbase_aws_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = TagbaseAwsCdkStack(app, "tagbase-aws-cdk")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
