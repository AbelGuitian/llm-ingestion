#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { LlmStack } from '../lib/llm-stack';

const app = new cdk.App();

const stage = process.env.NODE_ENV;

// require('custom-env').env(`${stage}`); // load environment variables

const id = `Marqo-LLM-150-${stage}`
if (stage === 'dev' || stage === 'development') {
  new LlmStack(app, id, {
    /* If you don't specify 'env', this stack will be environment-agnostic.
     * Account/Region-dependent features and context lookups will not work,
     * but a single synthesized template can be deployed anywhere. */

    /* Uncomment the next line to specialize this stack for the AWS Account
     * and Region that are implied by the current CLI configuration. */
    env: { account: process.env.CDK_DEFAULT_ACCOUNT, region: process.env.CDK_DEFAULT_REGION },

    /* Uncomment the next line if you know exactly what Account and Region you
     * want to deploy the stack to. */
    //env: { account: '698588432660', region: 'us-east-1' },

    /* For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html */
  })
} else if (stage === 'prod' || stage === 'production') {
  new LlmStack(app, id, {
    env: { account:  process.env.CDK_ACCOUNT, region: process.env.CDK_REGION },
  })
}