#!/usr/bin/env python3
import os

from aws_cdk import (
  Stack,
  aws_ec2,
)
from constructs import Construct

class VpcStack(Stack):

  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    #XXX: For createing Amazon MWAA in the existing VPC,
    # remove comments from the below codes and
    # comments out vpc = aws_ec2.Vpc(..) codes,
    # then pass -c vpc_name=your-existing-vpc to cdk command
    # for example,
    # cdk -c vpc_name=your-existing-vpc syth
    #
    vpc_name = self.node.try_get_context('vpc_name')
    self.vpc = aws_ec2.Vpc.from_lookup(self, 'ExistingVPC',
      # is_default=True,
      vpc_name=vpc_name
    )

    # self.vpc = aws_ec2.Vpc(self, 'DMSAuroraMysqlToS3VPC',
    #   max_azs=3,
    #   gateway_endpoints={
    #     "S3": aws_ec2.GatewayVpcEndpointOptions(
    #       service=aws_ec2.GatewayVpcEndpointAwsService.S3
    #     )
    #   }
    # )

