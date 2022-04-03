import os
from aws_cdk import core

# Singleton config object (don't access directly, use get_config below)
_config = None


def get_config():
    """Method to get the config from any location in the code."""
    global _config

    if _config is None:
        namespace_to_config_map = {
            "default": Config,
            "tagbase-dev": DevelopmentConfig,
            "tagbase-test": TestConfig,
            "tagbase": ProductionConfig,
        }

        _config = namespace_to_config_map.get(Config)()
    return _config


class Config(object):
    ENV = "default"
    PROJECT_NAME = os.environ.get("NAME", "tagbase-aws-cdk")
    VERSION = "0.1.0"
    TAG_PREFIX = "tagbase"

    VPC_ID = os.environ.get("VPC_ID", "")

    TAGBASE_DB_INSTANCE_IDENTIFIER = os.environ.get(
        "TAGBASE_DB_INSTANCE_IDENTIFIER", "tagbase"
    )
    TAGBASE_MASTER_USERNAME = os.environ.get("TAGBASE_MASTER_USERNAME", "")
    TAGBASE_DATABASE_NAME = os.environ.get("TAGBASE_DATABASE_NAME", "tagbase")
    TAGBASE_PREFERRED_MAINTENANCE_WINDOW = "Sun:05:00-Sun:06:00"
    TAGBASE_POSTGRES_SECURITY_GROUP = "tagbase-postgres-security-group"


class DevelopmentConfig(Config):
    ENV = "development"

    TAGBASE_COPY_TAGS_TO_SNAPSHOT = os.environ.get(
        "TAGBASE_COPY_TAGS_TO_SNAPSHOT", False
    )
    TAGBASE_BACKUP_RETENTION_DAYS = os.environ.get("TAGBASE_BACKUP_RETENTION_DAYS", 0)
    TAGBASE_POSTGRES_DELETION_PROTECTION = os.environ.get(
        "TAGBASE_POSTGRES_DELETION_PROTECTION", False
    )
    TAGBASE_CDK_REMOVAL_POLICY = core.RemovalPolicy.DESTROY
    TAGBASE_POSTGRES_INSTANCE_TYPE = os.environ.get(
        "TAGBASE_POSTGRES_INSTANCE_TYPE", "t3.small"
    )
    TAGBASE_POSTGRES_ALLOCATED_STORAGE = os.environ.get("allocated_storage", 20)
    # https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIOPS.StorageTypes.html#USER_PIOPS.Autoscaling
    TAGBASE_MAX_ALLOCATED_STORAGE = os.environ.get("TAGBASE_MAX_ALLOCATED_STORAGE", 200)
    TAGBASE_MASTER_USER_PASSWORD = os.environ.get("TAGBASE_MASTER_USER_PASSWORD", "")
    TAGBASE_POSTGRES_SECURITY_GROUP = Config.TAGBASE_POSTGRES_SECURITY_GROUP + "-" + ENV
    TAGBASE_POSTGRES_MULTI_AZ = False


class TestConfig(Config):
    ENV = "test"

    TAGBASE_COPY_TAGS_TO_SNAPSHOT = os.environ.get(
        "TAGBASE_COPY_TAGS_TO_SNAPSHOT", False
    )
    TAGBASE_BACKUP_RETENTION_DAYS = os.environ.get("TAGBASE_BACKUP_RETENTION_DAYS", 0)
    TAGBASE_POSTGRES_DELETION_PROTECTION = os.environ.get(
        "TAGBASE_POSTGRES_DELETION_PROTECTION", False
    )
    TAGBASE_CDK_REMOVAL_POLICY = core.RemovalPolicy.DESTROY
    TAGBASE_POSTGRES_INSTANCE_TYPE = os.environ.get(
        "TAGBASE_POSTGRES_INSTANCE_TYPE", "t3.small"
    )
    TAGBASE_POSTGRES_ALLOCATED_STORAGE = os.environ.get("allocated_storage", 20)
    # https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIOPS.StorageTypes.html#USER_PIOPS.Autoscaling
    TAGBASE_MAX_ALLOCATED_STORAGE = os.environ.get("TAGBASE_MAX_ALLOCATED_STORAGE", 200)
    TAGBASE_MASTER_USER_PASSWORD = os.environ.get("TAGBASE_MASTER_USER_PASSWORD", "")
    TAGBASE_POSTGRES_SECURITY_GROUP = Config.TAGBASE_POSTGRES_SECURITY_GROUP + "-" + ENV
    TAGBASE_POSTGRES_MULTI_AZ = False


class ProductionConfig(Config):
    ENV = "production"
    VPC_ID = os.environ.get("VPC_ID", "")

    TAGBASE_COPY_TAGS_TO_SNAPSHOT = os.environ.get(
        "TAGBASE_COPY_TAGS_TO_SNAPSHOT", True
    )
    TAGBASE_BACKUP_RETENTION_DAYS = os.environ.get("TAGBASE_BACKUP_RETENTION_DAYS", 30)
    TAGBASE_POSTGRES_DELETION_PROTECTION = os.environ.get(
        "TAGBASE_POSTGRES_DELETION_PROTECTION", True
    )
    TAGBASE_CDK_REMOVAL_POLICY = core.RemovalPolicy.SNAPSHOT
    TAGBASE_POSTGRES_INSTANCE_TYPE = os.environ.get(
        "TAGBASE_POSTGRES_INSTANCE_TYPE", "m5.4xlarge"
    )
    TAGBASE_POSTGRES_ALLOCATED_STORAGE = os.environ.get("allocated_storage", 100)
    # https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIOPS.StorageTypes.html#USER_PIOPS.Autoscaling
    TAGBASE_MAX_ALLOCATED_STORAGE = os.environ.get(
        "TAGBASE_MAX_ALLOCATED_STORAGE", 1000
    )
    TAGBASE_MASTER_USER_PASSWORD = os.environ.get("TAGBASE_MASTER_USER_PASSWORD", "")
    TAGBASE_POSTGRES_SECURITY_GROUP = Config.TAGBASE_POSTGRES_SECURITY_GROUP + "-" + ENV
    TAGBASE_POSTGRES_MULTI_AZ = True