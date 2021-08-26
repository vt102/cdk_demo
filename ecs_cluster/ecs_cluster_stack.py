from aws_cdk import (
    core,
    core as cdk,
    aws_cloudformation as cfn,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
)

v=1

class EcsClusterStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        vpc = ec2.Vpc.from_lookup(self, 'scratch2Vpc', vpc_id='vpc-092967d64650b476c')

        fg_task = ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
            image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample:latest"))
            # image=ecs.ContainerImage.from_registry("nginx:latest"))
            # image=ecs.ContainerImage.from_registry("httpd:latest"))
        service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, f'PtestEcsCluster{v}',
            cpu=512,
            memory_limit_mib=1024,
            task_image_options=fg_task,
            vpc=vpc)

        scaling = service.service.auto_scale_task_count(
            max_capacity=10
        )
        scaling.scale_on_cpu_utilization(
            f'CpuScaling{v}',
            target_utilization_percent=50,
            scale_in_cooldown=core.Duration.seconds(60),
            scale_out_cooldown=core.Duration.seconds(60),
        )
                                         
        # wh = cfn.CfnWaitConditionHandle(self, f'PtestWH{v}')
        # wc = cfn.CfnWaitCondition(self, f'PtestWC{v}',
        #                      count=1,
        #                      handle=wh.ref,
        #                      timeout='1800')
