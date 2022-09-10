#!/usr/bin/env python3
import os
import json

import boto3

import aws_cdk as cdk

from cdk_stacks import (
  VpcStack,
  AuroraMysqlStack,
  KinesisDataStreamStack,
  DMSAuroraMysqlToKinesisStack,
  OpenSearchStack,
  KinesisFirehoseStack
)


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
  kds_stack.kinesis_stream_arn
)

ops_stack = OpenSearchStack(app, 'OpenSearchStack',
  vpc_stack.vpc
)

firehose_stack = KinesisFirehoseStack(app, 'FirehoseStack',
  vpc_stack.vpc,
  kds_stack.kinesis_stream_arn,
  ops_stack.ops_domain_arn,
  ops_stack.ops_client_sg_id
)

app.synth()
