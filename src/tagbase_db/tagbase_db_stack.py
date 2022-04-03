from aws_cdk import core, aws_ec2 as ec2, aws_rds as rds
from src.config import get_config

config = get_config()


class TagbaseDBStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # vpc group for PostgreSQL
        vpc = ec2.Vpc.from_lookup(self, "tagbase-vpc", vpc_id=config.VPC_ID)

        security_group = ec2.SecurityGroup(
            self,
            config.TAGBASE_POSTGRES_SECURITY_GROUP,
            vpc=vpc,
            description="",
            allow_all_outbound=False,
        )

        # inbound rules
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(5432), "")
        security_group.add_ingress_rule(ec2.Peer.any_ipv6(), ec2.Port.tcp(5432), "")

        # outbound rules
        security_group.add_egress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(5432), "")
        security_group.add_egress_rule(ec2.Peer.any_ipv6(), ec2.Port.tcp(5432), "")

        # configure postgreSQL
        rds.DatabaseInstance(
            self,
            "Instance",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_13_4
            ),
            # optional, defaults to m5.large
            instance_type=ec2.InstanceType(config.TAGBASE_POSTGRES_INSTANCE_TYPE),
            multi_az=config.TAGBASE_POSTGRES_MULTI_AZ,
            # I THINK THESE ARE THE IAM SPECIFIC ROLES
            # domain_role=None,
            # cloudwatch_logs_retention_role=None,
            # END IAM SPECIFIC ROLES
            storage_type=rds.StorageType.GP2,
            allocated_storage=config.TAGBASE_POSTGRES_ALLOCATED_STORAGE,
            max_allocated_storage=config.TAGBASE_MAX_ALLOCATED_STORAGE,
            instance_identifier=config.TAGBASE_DB_INSTANCE_IDENTIFIER,
            credentials=rds.Credentials.from_password(
                config.TAGBASE_MASTER_USERNAME,
                core.SecretValue.plain_text(config.TAGBASE_MASTER_USER_PASSWORD),
            ),
            vpc=vpc,
            # if you want a public db
            # vpc_subnets={
            #     "subnet_type": ec2.SubnetType.PUBLIC # PRIVATE
            # },
            publicly_accessible=False,
            security_groups=[security_group],
            database_name=config.TAGBASE_DATABASE_NAME,
            port=5432,
            # parameter_group=default.postgres13, will this create one on its own if not set
            # parameter_group=rds.ParameterGroup(self, "ParameterGroup",
            #                                    engine=rds.DatabaseInstanceEngine.oracle_se2(
            #                                        version=rds.OracleEngineVersion.VER_19_0_0_0_2020_04_R1),
            #                                    parameters={
            #                                        "open_cursors": "2500"
            #                                    }
            #                                    )
            iam_authentication=False,
            storage_encrypted=False,
            backup_retention=core.Duration.days(config.TAGBASE_BACKUP_RETENTION_DAYS),
            copy_tags_to_snapshot=config.TAGBASE_COPY_TAGS_TO_SNAPSHOT,
            # monitoring_interval='' the default is false. Do we want this for PROD? - most likely Enhanced monitoring
            # THESE WILL CREATE NEW IAM CAUSING THE STACK NOT TO WORK AS PERMISSIONS TO CREATE NEW IAM ROLES ARE NOT ENABLED (cloudwatch_logs_exports, cloudwatch_logs_retention)
            # cloudwatch_logs_exports=['Postgresql log'], # ??? will this work?
            # cloudwatch_logs_retention=logs.RetentionDays.ONE_MONTH,
            auto_minor_version_upgrade=True,
            preferred_maintenance_window=config.TAGBASE_PREFERRED_MAINTENANCE_WINDOW,  # Sun:05:00-Sun:06:00
            deletion_protection=config.TAGBASE_POSTGRES_DELETION_PROTECTION,  # test False | Prod = True
            removal_policy=config.TAGBASE_CDK_REMOVAL_POLICY,
        )
