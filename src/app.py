#!/usr/bin/env python3
import os
from datetime import datetime

import aws_cdk as cdk

from config import get_config
from tagbase_db.tagbase_db_stack import TagbaseDBStack
from tagbase_vpc.tagbase_vpc_stack import TagbaseVPCStack

config = get_config()
env = cdk.Environment(
    account=os.getenv("TAGBASE_AWS_ACCOUNT"), region=os.getenv("TAGBASE_DEFAULT_REGION")
)

app = cdk.App()

tagbase_vpc_stack = TagbaseVPCStack(
    app,
    "tagbase-vpc-stack",
    env=env,
    description="Defines a VPC, a Public Subnet and Private Subnet with NAT Gateway.",
)
cdk.Tags.of(tagbase_vpc_stack).add(f"{config.TAG_PREFIX}:environment-type", config.ENV)
cdk.Tags.of(tagbase_vpc_stack).add(f"{config.TAG_PREFIX}:subsystem-name", "tagbase-vpc")
cdk.Tags.of(tagbase_vpc_stack).add(
    f"{config.TAG_PREFIX}:component-name", config.PROJECT_NAME
)
cdk.Tags.of(tagbase_vpc_stack).add(
    f"{config.TAG_PREFIX}:component-version", config.VERSION
)
cdk.Tags.of(tagbase_vpc_stack).add(
    f"{config.TAG_PREFIX}:component-modified", datetime.utcnow().isoformat()
)

tagbase_db_stack = TagbaseDBStack(
    app,
    "tagbase-db-stack",
    env=env,
    description="Defines a Security Group, Ingress and Egress rules, and a RDS PostgreSQL database.",
    new_vpc=tagbase_vpc_stack.vpc,
)
cdk.Tags.of(tagbase_db_stack).add(f"{config.TAG_PREFIX}:environment-type", config.ENV)
cdk.Tags.of(tagbase_db_stack).add(f"{config.TAG_PREFIX}:subsystem-name", "tagbase-db")
cdk.Tags.of(tagbase_db_stack).add(
    f"{config.TAG_PREFIX}:component-name", config.PROJECT_NAME
)
cdk.Tags.of(tagbase_db_stack).add(
    f"{config.TAG_PREFIX}:component-version", config.VERSION
)
cdk.Tags.of(tagbase_db_stack).add(
    f"{config.TAG_PREFIX}:component-modified", datetime.utcnow().isoformat()
)

app.synth()
