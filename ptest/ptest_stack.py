from aws_cdk import (
    core,
    core as cdk,
    aws_codecommit as codecommit,
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
                input=pipelines.CodePipelineSource.code_commit(
                    codecommit.Repository.from_repository_name(self, 'Repository', "cdk_demo"),
                    branch='main'),
                commands=[
                    'pip install -r requirements.txt',
                    'npm install -g aws-cdk',
                    # 'python -m venv .venv',
                    # '. .venv/bin/activate',
                    'cdk synth'
                ]))

        stg_build = p.add_stage(pipelines.Stage(self, 'TestBuild',
                                                synth=pipelines.ShellStep(
                                                    'SynthBuild',
                                                    command=[
                                                        'ls -al'
                                                    ])))
                                                    
        
        stg_preprod = p.add_stage(EcsClusterStage(self, 'PreProd',
                                                  env=cdk.Environment(account="989957622819", region="us-east-2")),
                                  post=[pipelines.ManualApprovalStep('PreProd Acceptance')]
                                  )
        
        stg_prod = p.add_stage(EcsClusterStage(self, 'Production',
                                               env=cdk.Environment(account="989957622819", region="us-east-2")))
