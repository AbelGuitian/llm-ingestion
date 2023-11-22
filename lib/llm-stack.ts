import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as path from "path";
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as s3n from 'aws-cdk-lib/aws-s3-notifications';
import * as pythonLambda from '@aws-cdk/aws-lambda-python-alpha';
import * as ec2 from "aws-cdk-lib/aws-ec2"


export class LlmStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

      //get VPC Info form AWS account, FYI we are not rebuilding we are referencing
      const DefaultVpc = ec2.Vpc.fromVpcAttributes(this, 'vpcdev', {
          vpcId:'vpc-0c8e44051b2784f11',
          availabilityZones: ['us-east-1a'],
          privateSubnetIds: ['subnet-05311cc6f18e34ca2'],
          publicSubnetIds: ['subnet-06c4dbb2372efe26a']
      });

      const pyFn = new pythonLambda.PythonFunction(this, 'PythonFunction', {
          entry: path.join(__dirname, '../lambda/python'),
          index: 'manage-s3-event-notifications.py',
          handler: 'handler',
          runtime: lambda.Runtime.PYTHON_3_11,
          timeout: cdk.Duration.seconds(30),
          retryAttempts: 1,
          vpc: DefaultVpc,
          bundling: {
              assetExcludes: ['.venv'],
          }
      });


    const fn = new lambda.Function(this, 'S3EventNotificationsLambda', {
      runtime: lambda.Runtime.NODEJS_20_X,
      functionName: 'S3EventNotificationsManager',
      handler: 'manage-s3-event-notifications.handler',
      code: lambda.Code.fromAsset(path.join(__dirname, '../lambda/typescript')),
      //reservedConcurrentExecutions: 1,
      timeout: cdk.Duration.seconds(30)
    });

    const bucket = new s3.Bucket(this, 'Bucket', {
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    bucket.grantRead(fn);
    bucket.grantRead(pyFn);

    bucket.addEventNotification(s3.EventType.OBJECT_CREATED, new s3n.LambdaDestination(pyFn), {suffix: '.pdf'});
    //bucket.addEventNotification(s3.EventType.OBJECT_CREATED, new s3n.LambdaDestination(pyFn), {suffix: '.pdf'});
  }
}
