#!/usr/bin/env python3
import os

from aws_cdk import (
    core,
    core as cdk,
    aws_cloudformation as cfn,
)

from ptest.ptest_stack import PtestStack

app = core.App()

PtestStack(app, "PtestStack",
           env=cdk.Environment(account="989957622819", region="us-east-2"),
           )

app.synth()
