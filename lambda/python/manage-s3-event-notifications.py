import marqo
import boto3
import helpers
from botocore.response import StreamingBody


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

    # trying to retrieve an object from s3
    """ s3_client = boto3.client('s3')

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

        helpers.print_content(file_content_bytes)  """

    return {
        'statusCode': 200,
        'body': event
    }


# handler({}, {})
