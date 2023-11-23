import marqo
import boto3
import helpers
from botocore.response import StreamingBody
from typing import Dict


def marqo_test():
    print('trying to connect to marqo')
    mq = marqo.Client(url='http://10.229.19.93')
    results = mq.index('jsr_hr_6_3_1_lm_l6').search(
        q='Hoy many context do you have?',
        limit=100,
        searchable_attributes=["Title", "Content"],
        show_highlights=True,
        search_method=marqo.SearchMethods.TENSOR
    )
    indexes = mq.get_indexes()

    print("xxx")
    print(results)


def handler(event, context):
    # save event to logs
    print(event)
    print('context: ', context)

    marqo_test()

    # for local testing
    # session = boto3.Session(profile_name='698588432660_KBIDeveloperAccess')
    # s3_client = session.client('s3')

    # trying to retrieve an object from s3
    s3_client = boto3.client('s3')

    for record in event['Records']:
        if record['eventName'] != 'ObjectCreated:Put':
            print('event name: ', record['eventName'])
            continue
        bucket_name = record['s3']['bucket']['name']
        object_name = record['s3']['object']['key']
        print('bucket_name: ', bucket_name)
        print('object_name: ', object_name)

        s3_object: StreamingBody = s3_client.get_object(Bucket=bucket_name, Key=object_name)['Body']
        file_content_bytes = s3_object.read()

        helpers.print_content(file_content_bytes)

    return {
        'statusCode': 200,
        'body': event
    }

# testing
# test_event = {'Records': [
#     {'eventVersion': '2.1', 'eventSource': 'aws:s3', 'awsRegion': 'us-east-1', 'eventTime': '2023-11-22T04:17:56.332Z',
#      'eventName': 'ObjectCreated:Put', 'userIdentity': {'principalId': 'AWS:AROA2FJY5REKHBMW5QBJW:a.nolascoguitian'},
#      'requestParameters': {'sourceIPAddress': '201.175.104.168'},
#      'responseElements': {'x-amz-request-id': 'REEKRN0E8B84EMEQ',
#                           'x-amz-id-2': 'ILjkRc5h0g+0TXbY2iHrMyuntVVgLLHx8z'
#                                         '/7ClcT7ApOxptOYRJA1lfvdXtnZcuafaErOpjSfTe3endf8rieLRYSSzAFW+Vi'},
#      's3': {'s3SchemaVersion': '1.0', 'configurationId': 'NTQ1YzRiOGUtMWIxZi00MjYwLWJhNTMtYTQ0MGEyMDcwNTg2',
#             'bucket': {'name': 'marqo-llm-150-bucket83908e77-ojofkpqesy6y',
#                        'ownerIdentity': {'principalId': 'ASGR0QQBM5VR5'},
#                        'arn': 'arn:aws:s3:::marqo-llm-150-bucket83908e77-ojofkpqesy6y'},
#             'object': {'key': 'DESCANSOS+DE+JUGADORES+1.pdf', 'size': 42150, 'eTag': '72426190cb03076b14883e80430d3dc9',
#                        'sequencer': '00655D80F445423794'}}}]}
#
# handler(test_event, {})
