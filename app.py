#!/usr/bin/env python3
import os
import json

import boto3

import aws_cdk as cdk

from cdk_stacks.vpc import VpcStack
from cdk_stacks.aurora_mysql import AuroraMysqlStack
from cdk_stacks.kds import KinesisDataStreamStack
from cdk_stacks.dms_aurora_mysql_to_kinesis import DMSAuroraMysqlToKinesisStack
from cdk_stacks.ops import OpenSearchStack
from cdk_stacks.firehose import KinesisFirehoseStack

app = cdk.App()

vpc_stack = VpcStack(app, 'VpcStack',
  env=cdk.Environment(
    account=os.environ["CDK_DEFAULT_ACCOUNT"],
    region=os.environ["CDK_DEFAULT_REGION"]))

aurora_mysql_stack = AuroraMysqlStack(app, 'AuroraMysqlStack',
  vpc_stack.vpc
)

kds_stack = KinesisDataStreamStack(app, 'DMSTargetKinesisDataStreamStack')

dms_stack = DMSAuroraMysqlToKinesisStack(app, 'DMSAuroraMysqlToKinesisStack',
  vpc_stack.vpc,
  aurora_mysql_stack.sg_mysql_client,
  kds_stack.kinesis_stream.stream_name
)

ops_stack = OpenSearchStack(app, 'OpenSearchStack',
  vpc_stack.vpc
)

firehose_stack = KinesisFirehoseStack(app, 'FirehoseStack',
  vpc_stack.vpc,
  kds_stack.kinesis_stream.stream_name,
  ops_stack.ops_domain_arn,
  ops_stack.ops_client_sg_id
)

app.synth()
