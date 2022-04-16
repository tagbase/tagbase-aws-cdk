from aws_cdk import aws_ec2 as ec2, aws_ssm as ssm, Stack
from constructs import Construct

from config import get_config

config = get_config()


class TagbaseVPCStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        env_name = config.ENV

        self.vpc = ec2.Vpc(
            self,
            config.VPC_ID,
            cidr="10.10.0.0/16",
            max_azs=2,
            enable_dns_hostnames=True,
            enable_dns_support=True,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public-Subnet",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=26,
                ),
                ec2.SubnetConfiguration(
                    name="Private-Subnet-with-Nat-Gateway",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                    cidr_mask=26,
                ),
            ],
            nat_gateways=1,
        )
        private_subnets = [subnet.subnet_id for subnet in self.vpc.private_subnets]

        count = 1
        for psub in private_subnets:
            ssm.StringParameter(
                self,
                "private-subnet-" + str(count),
                string_value=psub,
                parameter_name="/"
                + env_name
                + "/private-subnet-with-nat-gateway"
                + str(count),
            )
            count += 1
