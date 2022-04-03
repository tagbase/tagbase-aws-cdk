#!/usr/bin/env python3
import os
from datetime import datetime

import aws_cdk as cdk

from src.config import get_config

from src.tagbase_db.tagbase_db_stack import TagbaseDBStack

config = get_config()
env = cdk.Environment(
    account=os.getenv("TAGBASE_AWS_ACCOUNT"), region=os.getenv("TAGBASE_DEFAULT_REGION")
)

app = cdk.App()

tagbase_db_stack = TagbaseDBStack(app, "tagbase-db-stack", env=env)
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
