#!/usr/bin/env python3

import json

import boto3
import botocore

import aws_cdk as cdk

from aws_cdk import (
  Stack,
  aws_iam
)
from constructs import Construct

class DmsIAMRolesStack(Stack):

  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    iam_client = boto3.client('iam')

    try:
      iam_client.get_role(RoleName='dms-vpc-role')
      dms_vpc_role = aws_iam.Role.from_role_name(self, 'DMSVpcRole', role_name='dms-vpc-role')
    except iam_client.exceptions.NoSuchEntityException as ex:
      dms_vpc_role = aws_iam.Role(self, 'DMSVpcRole',
        role_name='dms-vpc-role',
        assumed_by=aws_iam.ServicePrincipal('dms.amazonaws.com'),
        managed_policies=[
          aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AmazonDMSVPCManagementRole'),
        ]
      )

    try:
      dms_cloudwatch_logs_role = aws_iam.Role.from_role_name(self, 'DMSCloudWatchLogsRole', role_name='dms-cloudwatch-logs-role')
    except iam_client.exceptions.NoSuchEntityException as ex:
      dms_cloudwatch_logs_role = aws_iam.Role(self, 'DMSCloudWatchLogsRole',
        role_name='dms-cloudwatch-logs-role',
        assumed_by=aws_iam.ServicePrincipal('dms.amazonaws.com'),
        managed_policies=[
          aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AmazonDMSCloudWatchLogsRole'),
        ]
      )

    cdk.CfnOutput(self, f'{self.stack_name}_DMSVpcRole', value=dms_vpc_role.role_arn)
    cdk.CfnOutput(self, f'{self.stack_name}_DMSCloudWatchLogsRole', value=dms_cloudwatch_logs_role.role_arn)
