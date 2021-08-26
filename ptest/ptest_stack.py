from aws_cdk import (
    core,
    core as cdk,
    pipelines,
)

from ecs_cluster import ecs_cluster_stack

class EcsClusterStage(cdk.Stage):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        service = ecs_cluster_stack.EcsClusterStack(self, 'PtestEcsCluster')
    

class PtestStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        p = pipelines.CodePipeline(
            self, 'PtestStackCodePipeline',
            synth=pipelines.ShellStep(
                'Synth',
                input=pipelines.CodePipelineSource.git_hub("vt102/cdk_demo", "main"),
                commands=[
                    'npm install -g aws-cdk',
                    'python -m venv .venv',
                    '. .venv/bin/activate',
                    'pip install -r requirements.txt',
                    'cdk synth'
                ]))
        p.add_stage(EcsClusterStage(self, 'PreProd',
                               env=cdk.Environment(account="989957622819", region="us-east-2")))
