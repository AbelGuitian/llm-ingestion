// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

/*import {
    S3Client,
    GetBucketNotificationConfigurationCommand,
    PutBucketNotificationConfigurationCommand
} from "@aws-sdk/client-s3";*/
//const s3Client = new S3Client([ {region: process.env.AWS_REGION}] );

// const url = require('url');
// const https = require('https');

exports.handler = async function (event: any, context: any) {
    log(JSON.stringify(event, undefined, 2));

    function log(obj: any) {
        console.log(event.RequestId, event.StackId, event.LogicalResourceId, obj);
    }
};