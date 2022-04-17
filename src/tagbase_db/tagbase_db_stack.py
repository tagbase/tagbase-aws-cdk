from aws_cdk import aws_ec2 as ec2, aws_rds as rds, Stack, SecretValue, Duration
from constructs import Construct

from config import get_config

config = get_config()


class TagbaseDBStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, new_vpc: ec2.Vpc, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        if new_vpc is not None:
            vpc = new_vpc
        else:
            vpc = ec2.Vpc.from_lookup(self, "tagbase-vpc", vpc_id=config.VPC_ID)

        security_group = ec2.SecurityGroup(
            self,
            config.TAGBASE_POSTGRES_SECURITY_GROUP,
            vpc=vpc,
            description="Security group for facilitating access to TagbaseDB.",
            allow_all_outbound=False,
        )

        # inbound rules
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(5432), "")
        security_group.add_ingress_rule(ec2.Peer.any_ipv6(), ec2.Port.tcp(5432), "")

        # outbound rules
        security_group.add_egress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(5432), "")
        security_group.add_egress_rule(ec2.Peer.any_ipv6(), ec2.Port.tcp(5432), "")

        # configure PostgreSQL
        rds.DatabaseInstance(
            self,
            "Instance",
            allocated_storage=config.TAGBASE_POSTGRES_ALLOCATED_STORAGE,
            auto_minor_version_upgrade=True,
            backup_retention=Duration.days(config.TAGBASE_BACKUP_RETENTION_DAYS),
            deletion_protection=config.TAGBASE_POSTGRES_DELETION_PROTECTION,  # test False | Prod = True
            copy_tags_to_snapshot=config.TAGBASE_COPY_TAGS_TO_SNAPSHOT,
            credentials=rds.Credentials.from_password(
                config.TAGBASE_MASTER_USERNAME,
                SecretValue.plain_text(config.TAGBASE_MASTER_USER_PASSWORD),
            ),
            database_name=config.TAGBASE_DATABASE_NAME,
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_13_4
            ),
            iam_authentication=False,
            instance_identifier=config.TAGBASE_DB_INSTANCE_IDENTIFIER,
            instance_type=ec2.InstanceType(config.TAGBASE_POSTGRES_INSTANCE_TYPE),
            multi_az=config.TAGBASE_POSTGRES_MULTI_AZ,
            max_allocated_storage=config.TAGBASE_MAX_ALLOCATED_STORAGE,
            port=5432,
            preferred_maintenance_window=config.TAGBASE_PREFERRED_MAINTENANCE_WINDOW,
            publicly_accessible=False,
            removal_policy=config.TAGBASE_CDK_REMOVAL_POLICY,
            security_groups=[security_group],
            storage_encrypted=False,
            storage_type=rds.StorageType.GP2,
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnets=vpc.select_subnets(
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT
                ).subnets
            ),
        )
